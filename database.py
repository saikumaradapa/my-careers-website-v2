from flask import jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load database credentials from environment variables
db_data = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}

def get_connection():
    return mysql.connector.connect(
        user=db_data['user'],
        password=db_data['password'],
        host=db_data['host'],
        port=int(db_data['port']),  
        database=db_data['database']
    )

def load_jobs_from_db():
    connection = get_connection()  # Establish a new connection each time
    cursor = connection.cursor()
    query = "SELECT * FROM jobs"
    cursor.execute(query)
    jobs = []
    for (id, title, location, salary, currency, responsibilities, requirements) in cursor:
        jobs.append({
            'id': id,
            'title': title,
            'location': location,
            'salary': salary,
            'currency': currency,
            'responsibilities': responsibilities,
            'requirements': requirements
        })
    cursor.close()
    connection.close()  # Close the connection after use
    return jobs


def load_job_with_id(id):
    connection = get_connection()  # Establish a new connection each time
    cursor = connection.cursor()
    query = "SELECT * FROM jobs WHERE id = %s"
    
    cursor.execute(query, (id,))
    job = cursor.fetchone()  # Fetch the single result immediately
    
    cursor.close()
    connection.close()  # Close the connection after use
    
    if job:
        return {
            'id': job[0],
            'title': job[1],
            'location': job[2],
            'salary': job[3],
            'currency': job[4],
            'responsibilities': job[5],
            'requirements': job[6]
        }
    return None  # Return None if no job is found with the given id




def insert_job(job):
    connection = get_connection()  # Establish a new connection for insertion
    cursor = connection.cursor()
    query = ("INSERT INTO jobs "
             "(title, location, salary, currency, responsibilities, requirements) "
             "VALUES (%s, %s, %s, %s, %s, %s)")
    
    data = (job['title'], job['location'], job['salary'], job['currency'], job['responsibilities'], job['requirements'])
    cursor.execute(query, data)
    connection.commit()
    
    last_id = cursor.lastrowid
    cursor.close()
    connection.close()  # Close the connection after use
    return last_id


def add_application_to_db(job_id, application):
    connection = get_connection()
    cursor = connection.cursor()
    query = ("INSERT INTO applications "
            "(job_id, full_name, email, linkedin_url, education, experience, resume_url)"
             "VALUES (%s, %s, %s, %s, %s, %s, %s);")
    data = (job_id, application['full_name'], application['email'], application['linkedin_url'], application['education'], application['experience'], application['resume_url'])
    cursor.execute(query, data)
    connection.commit()

    last_id = cursor._last_insert_id
    cursor.close()
    return last_id

def load_applications_from_db():
    connection = get_connection()  # Establish a new connection each time
    cursor = connection.cursor()

    query = """
    SELECT id, job_id, full_name, email, linkedin_url, education, experience, resume_url, created_at, updated_at 
    FROM applications
    """

    cursor.execute(query)
    applications = []

    for (id, job_id, full_name, email, linkedin_url, education, experience, resume_url, created_at, updated_at) in cursor:
        applications.append({
            'id': id,
            'job_id': job_id,
            'full_name': full_name,
            'email': email,
            'linkedin_url': linkedin_url,
            'education': education,
            'experience': experience,
            'resume_url': resume_url,
            'created_at': created_at,
            'updated_at': updated_at
        })

    cursor.close()
    connection.close()

    return applications


def get_columns(table_name):
    connection = get_connection()  # Establish a new connection each time
    cursor = connection.cursor()
    query = "SHOW COLUMNS FROM " + table_name
    cursor.execute(query)
    columns = [column[0] for column in cursor.fetchall()]
    return columns

if __name__ == '__main__':
    # print(load_applications_from_db(), end='\n\n\n')
    print(get_columns('applications'))