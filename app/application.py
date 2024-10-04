from flask import Flask, redirect, url_for, request, render_template, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import logging, os, uuid

# Defining global path variables
CWD = os.path.dirname(os.path.abspath(__file__))
OS = "/" if os.name == "nt" else "/"

# Defining variables for flask
load_dotenv()
app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = os.environ.get('SECRET_KEY', uuid.uuid4())
app.logger.setLevel(logging.INFO)

# Defining variables for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + f"{CWD}{OS}database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Login_Manager = LoginManager(app)
bcrypt = Bcrypt(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))


# User callback for current session
@Login_Manager.user_loader
def load_user(id):
    '''
    Retrieves the current user session based on the unique identifier

    Args:
        id (int): Unique identifier of current user

    Returns:
        Object of current User session  
    '''
    return db.session.get(User, int(id))


def authenticate(username, password):
    '''
    This function authenticates a user by checking their username and password against the database.
    It uses Flask's bcrypt module to check the password hash against the database.

    Args:
        username (str): Username.
        password (str): Password.

    Returns:
        bool: True if login succesful, False if login unsuccesful
    '''
    # Query the username out of the database 
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password=password):
        app.logger.info(f"the user '{username}' logged in successfully with password '{password}'")
        login_user(user)
        return True
    
    app.logger.warning(f"the user '{ username }' failed to log in '{ password }'")
    return False


@app.route("/")
def index():
    '''
    The index function returns the rendered template "index.html" with the authentication status of
    the current user.

    Returns:
        Render template of index.html
    '''
    return render_template("index.html", is_authenticated=current_user.is_authenticated)

@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Checks if the request method is POST, retrieves the username and password from
    the form, authenticates the user and redirects to the index page if successful. Otherwise renders
    the login template.

    Returns:
        Render template for index.html if login was succeful. Else returns the login page.
    '''
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if authenticate(username, password):
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    '''
    Logs out user.

    Returns:
        Redirects user to index.html
    '''
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    '''
    Checks if a username already exists in the database, generates a
    password hash and adds a new user to the database if the username is unique.
    
    Returns:
        Redirects user to login page if succesful. Otherwise, returns register page.
    '''
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username already exists in db
        user = User.query.filter_by(username=username).first()

        # If user does exist, return to register template
        if user:
            flash("Username already exists")
            return render_template('register.html')
        
        # Generate password hash
        PasswordHash = bcrypt.generate_password_hash(password, 10).decode('utf-8')
        NewUser = (User(username=username, password=PasswordHash))

        db.session.add(NewUser)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
