from flask import Flask, render_template, request, jsonify
from database import load_jobs_from_db
from database import load_job_from_db, add_application_to_db

app = Flask(__name__)


@app.route("/")
def hello_world():
    jobs = load_jobs_from_db()
    return render_template("home.html",
                           jobs=jobs,
                           company_name="Happy Careers")


@app.route('/faqs')
def faqs():
    return render_template('faq.html')


@app.route('/features')
def features():
    return render_template('features.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)


@app.route("/job/json/<id>")
def show_job(id):
    job = load_job_from_db(id)
    if not job:
        return "Not Found", 404
    return jsonify(job)


@app.route("/job/<id>")
def show_job_det(id):
    job = load_job_from_db(id)
    if not job:
        return "Not Found", 404
    return render_template('jobpage.html', job=job)


@app.route("/job/json/<id>/apply")
def apply_to_json_job(id):
    data = request.args
    return jsonify(data)


@app.route("/job/<id>/apply", methods=["POST"])
def apply_to_job(id):
    job = load_job_from_db(id)
    # store this in DB
    # send an email
    # display an acknowledgemnet
    data = request.form
    add_application_to_db(id, data)
    return render_template('application_submitted.html',
                           application=data,
                           job=job)


if __name__ == "__main__":
    print("I am inside if now")
    app.run(host="0.0.0.0", debug=True)
