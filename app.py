from flask import Flask, redirect, render_template, jsonify, request, url_for, session
import os
from database import *
import time

app = Flask(__name__)

app.secret_key = os.getenv('MY_SECRET_KEY')

@app.route('/')
def index():
    jobs = load_jobs_from_db()
    return render_template('index.html', jobs=jobs)

@app.route('/api/jobs')
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)

@app.route('/job/<int:id>')
def show_job(id):
    job = load_job_with_id(id)
    if not job:
        text = "Please go back to the Homepage to see the list of our open positions"
        return render_template('not_found_page.html', text=text), 404
    return render_template('jobpage.html', job=job)

@app.route('/job/<int:id>/apply', methods=['POST'])
def job_apply(id):
    application = request.form
    application_id = add_application_to_db(id, application)
    session['application_id'] = application_id
    session['timestamp'] = time.time()  # Store the time the session was created

    if session['application_id']:
        return redirect(url_for('job_apply_success', id=application_id))
    else:
        return redirect(url_for('job_apply_error'))

@app.route('/api/applications')
def list_applications():
    applications = load_applications_from_db()
    return jsonify(applications)

@app.route('/applications')
def show_applications():
    applications = load_applications_from_db()
    return render_template('applications_dashboard.html', applications=applications)

@app.route('/job/<int:id>/success')
def job_apply_success(id):
    # Check if the session is still valid (10 seconds)
    current_time = time.time()
    if 'timestamp' in session and current_time - session['timestamp'] > 10:
        session.pop('application_id', None)
        session.pop('timestamp', None)

    if id == session.get('application_id'):
        application = load_application_with_id(id)
        return render_template('application_send.html', application=application)
    else:
        return redirect(url_for('index'))

@app.route('/job/apply/error')
def job_apply_error():
    text = "error occurred while applying for the job"
    return render_template('not_found_page.html', text=text), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
