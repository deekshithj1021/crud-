from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    house = db.Column(db.String(100))
    heritage = db.Column(db.String(100))

    def __init__(self, name, house, heritage):
        self.name = name
        self.house = house
        self.heritage = heritage


# This is the index route where we are going to
# query on hogwarts student data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", students=all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        house = request.form['house']
        heritage = request.form['heritage']

        my_data = Data(name, house, heritage)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Inserted Successfully")

        return redirect(url_for('Index'))


# this is our update route where we are going to update student data
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.house = request.form['house']
        my_data.heritage = request.form['heritage']

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('Index'))


# This route is for deleting student records
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)