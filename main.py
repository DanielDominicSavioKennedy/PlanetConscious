from flask import *
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)

app.config["SECRET_KEY"] = "WebsiteMadeByWebLaunch2022"

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

db.create_all()

activites = []

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/table", methods=["GET", "POST"])
def table():
    if request.method == "POST":
        status = request.form.get("status")
        time_status, date_status = '', ''
        if status == "2":
            now = datetime.datetime.now().time()
            time = now.strftime("%H:%M:%S")
            now = datetime.datetime.now().date()
            date = now.strftime("%Y-%m-%d")
            time_status=time
            date_status = date
        elif status == "1":
            time_status, date_status = "Pending", "Pending"
        else:
            time_status, date_status = "Incomplete", "Incomplete"

        activites.append({
            "s.no":len(activites)+5,
            "activity":request.form.get("activity"), 
            "time":time_status,
            "date":date_status
            })
        return redirect("table")
    print(activites)
    return render_template("tables-general.html", activites=activites)

@app.route("/chart")
def chart():
    return render_template("charts.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")

        if User.query.filter_by(email=email).first():
            flash("User already registered, Please login instead!")
            return redirect(url_for('login'))

        name, password = request.form.get("name"), request.form.get("password")
        new_user = User(
            name = name,
            email = email,
            password = password,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            password = request.form.get("password")
            if user.password == password:
                return redirect(url_for("home"))
 
            flash("Invalid password")
            return redirect(url_for("login"))

        flash("User not registered with email!")
        return redirect(url_for("login"))
    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)