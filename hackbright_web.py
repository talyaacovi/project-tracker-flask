"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect, session, url_for

import hackbright
# importing hackbright.py which is accessing our database
# hackbright_web.py is our server program

app = Flask(__name__)
app.secret_key = "SEEEKRIT"


@app.route("/student")
def get_student():
    """Show information about a student."""

    # github = "jhacks"
    github = request.args.get('github')

    # first, last, github = hackbright.get_student_by_github(github)
    student = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    if student:
        first, last, github = student

        return render_template('student_info.html',
                               first=first,
                               last=last,
                               github=github,
                               grades=grades)
    else:
        # session['github'] = github
        return redirect(url_for("get_add_form", github=github))

    # "{acct} is the GitHub account for {first} {last}".format(
        # acct=github, first=first, last=last)


@app.route('/student-search')
def get_student_form():
    """Show form for searching for a student."""

    return render_template('student_search.html')


@app.route('/student-add', methods=['POST'])
def student_add():
    """Add a new student to the database."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template('success.html', first_name=first_name, github=github)
    # this route will be called from the form action
    # and redirect to /student route


@app.route('/add')
def get_add_form():
    """Show form for adding a new student."""

    github = request.args.get("github")

    if not github:
        github = ""

    return render_template('student-add.html', github=github)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
