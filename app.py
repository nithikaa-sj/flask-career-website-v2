from flask import Flask, render_template, request, jsonify, redirect, flash
from database import load_jobs_from_db
from database import load_job_from_db, add_application_to_db
from mailjet_rest import Client
import os
import requests

mailjet = Client(auth=(os.environ['MAILJET_API_KEY'],
                       os.environ['MAILJET_SECRET_KEY']),
                 version='v3.1')

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "devkey") 




@app.route("/")
def hello_world():
    jobs = load_jobs_from_db()
    return render_template("home.html",
                           jobs=jobs,
                           company_name="Happy Careers")


def send_email(to_email, to_name, subject, body):
    data = {
        'Messages': [{
            "From": {
                "Email": "mirthulajagadesh@gmail.com",
                "Name": "Happy Careers"
            },
            "To": [{
                "Email": to_email,
                "Name": to_name
            }],
            "Subject": subject,
            "TextPart": body,
            "HTMLPart": body,
            "CustomID": "AppGettingStartedTest"
        }]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())


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

    # 1. Get hCaptcha token from form
    hcaptcha_response = data.get("h-captcha-response")
    secret = os.environ.get(
        "HCAPTCHA_SECRET_KEY")  # set this in Render Environment tab

    # 2. Verify with hCaptcha server
    hcaptcha_verify_url = "https://hcaptcha.com/siteverify"
    hcaptcha_data = {"secret": secret, "response": hcaptcha_response}

    result = requests.post(hcaptcha_verify_url, data=hcaptcha_data).json()

    # 3. Check success
    if not result.get("success"):
        print("hCaptcha failed:", result)
        # If hCaptcha fails, redirect or show error
        flash("hCaptcha verification failed. Please try again.")
        return redirect(request.referrer or "/")

    add_application_to_db(id, data)

    send_email(
        to_email=data['email'],
        to_name=data['fullname'],
        subject="Happy Careers Application Confirmation",
        body=
        f"Hi {data['fullname']},<br><br>Thank you for applying to {job['title']} at Happy Careers.<br><br>We will be in touch soon!<br><br>Best regards,<br>Happy Careers Team"
    )

    send_email(
        to_email="nithikaajagadesh@gmail.com",
        to_name="Admin",
        subject=f"{data['fullname']} has applied for {job['title']}",
        body=
        f"New Application received:\n\nName: {data['fullname']}\nEmail: {data['email']}\nLinkedIn: {data['linkedin']}\nEducation: {data['education']}\nWork Experience: {data['work_experience']}"
    )

    return render_template('application_submitted.html',
                           application=data,
                           job=job)


if __name__ == "__main__":
    print("I am inside if now")
    app.run(host="0.0.0.0", debug=True)
