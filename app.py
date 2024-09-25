from flask import Flask, render_template, jsonify, request
from database import *

app = Flask(__name__)

@app.route('/')
def hello_world():    
    jobs = load_jobs_from_db() 
    return render_template('index.html', 
                           jobs=jobs,
                           )

@app.route('/api/jobs')
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)

@app.route('/job/<id>')
def show_job(id):
   job = load_job_with_id(id)
   if not job:
      text = "Please go back to the Homepage to see the list of our open positions"
      return render_template('not_found_page.html', 
                             text=text), 404
   return render_template('jobpage.html',
                          job=job)

@app.route('/job/<id>/apply', methods=['post'])
def test(id):
   job=load_job_with_id(id)
   application = request.form
   add_application_to_db(id, application)
   return render_template('application_send.html', 
                          job=job,
                          application=application
                          )

@app.route('/api/applications')
def list_applications():
    applications = load_applications_from_db()
    return jsonify(applications)

@app.route('/applications')
def show_applications():
    applications = load_applications_from_db()
    return render_template('applications_dashboard.html', 
                           applications=applications,
                           )


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)