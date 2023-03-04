from flask import *
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps


app = Flask(__name__)

app.config["SECRET_KEY"] = "WebsiteMadeByWebLaunch2022"

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

db.create_all()

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

activites = []

@app.route("/home")
@login_required
def home():
    return render_template("index.html", current_user=current_user)

@app.route("/table", methods=["GET", "POST"])
@login_required
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
    return render_template("tables-general.html", current_user=current_user, activites=activites)

@app.route("/chart")
@login_required
def chart():
    return render_template("charts.html", current_user=current_user)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", current_user=current_user)

@app.route("/blog")
@login_required
def blog():
    return render_template("blogs.html", current_user=current_user)

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
        login_user(new_user)
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
                login_user(user)
                return redirect(url_for("home"))
 
            flash("Invalid password")
            return redirect(url_for("login"))

        flash("User not registered with email!")
        return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)