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

if __name__ == '__main__':
    # Test loading jobs
    jobs = load_jobs_from_db()
    print(jobs, end='\n\n')

    # Test inserting a new job (Optional example, uncomment to use)
    new_job = {
        'title': 'Full Stack Developer',
        'location': 'Remote',
        'salary': 90000,
        'currency': '$',
        'responsibilities': 'Develop and maintain the full stack web application',
        'requirements': 'Experience in React.js and Node.js'
    }
    job_id = insert_job(new_job)
    print(f"New job inserted with ID: {job_id} \n\n")
    print(load_jobs_from_db())
