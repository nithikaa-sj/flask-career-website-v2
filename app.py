from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [{
    'id': 1,
    'title': "Data Analyst",
    'location': "Bengaluru, India",
    'salary': "Rs. 10,00,000"
}, {
    'id': 2,
    'title': "Data Scientist",
    'location': "Delhi, India",
    'salary': "Rs. 15,00,000"
}, {
    'id': 3,
    'title': "Frontend Engineer",
    'location': "Remote",
    'salary': "Rs. 12,00,000"
}, {
    'id': 4,
    'title': "Backend Engineer",
    'location': "San Francisco, USA",
}]


@app.route("/")
def hello_world():
  return render_template("home.html", jobs=JOBS, company_name="Happy Careers")

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
  return jsonify(JOBS)





if __name__ == "__main__":
  print("I am inside if now")
  app.run(host="0.0.0.0", debug=True)
