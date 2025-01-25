from flask import Flask, request, render_template, redirect, url_for, flash, session, abort
import os
import pymysql
from sqlalchemy.orm import sessionmaker
from tabledef import *
from config import config
from sqlalchemy.exc import OperationalError

engine = create_engine('mysql+mysqlconnector://user:pass@localhost:3306/dummydata', echo=True)

app = Flask(__name__)
app.secret_key = 'CS Internship'

def get_db_connection():
    return pymysql.connect(
        host=config['host'],
        user=config['username'],
        password=config['password'],
        database=config['database']
    )

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([username]), User.password.in_([password]) )
        result = query.first()
        if result:  # Temporary auth logic
            session['username'] = username
            return redirect(url_for("database"))
        else:
            flash("Invalid username or password", "error")
    return render_template("index.html")

@app.route("/database")
def database():
    sql = "SELECT * FROM experiences"
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            experiences = cursor.fetchall()  # Fetch all rows as a list of dictionaries
    except OperationalError as e:
        return f"Connection failed: {str(e)}", 500
    finally:
        connection.close()
    return render_template("database.html", experiences=experiences)

@app.route("/view-post")
def viewpost():
    item_id = request.args.get('item_id')
    sql = "SELECT * FROM experiences WHERE id = %s"
    connection = get_db_connection()
    if (session['username'] == None):
        return redirect("/")
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (item_id,))  # Execute query with parameter
            experience = cursor.fetchone()
    except OperationalError as e:
        return f"Connection failed: {str(e)}", 500
    finally:
        connection.close()
    if (experience):
        return render_template("view-post.html", experience=experience)
    else:
        return "Experience not found", 404

@app.route("/search", methods=["GET"])
def search():
    search = request.args.get('searchbar')
    sql = "SELECT * FROM experiences WHERE keywords LIKE %s"
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, ('%'+ search + '%',))  # Execute query with parameter
            experiences = cursor.fetchall()
    except OperationalError as e:
        return f"Connection failed: {str(e)}", 500
    finally:
        connection.close()
    return render_template("database.html", experiences=experiences)

@app.route("/logout")
def logout():
    session['username'] = None
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)