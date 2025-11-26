from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB


class User(db.Model, UserMixin, UserWarning):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    print(f"My name is {request.form.get('name')} and my email is {request.form.get('email')}")
    password = request.form.get('password')
    pass_scry = generate_password_hash(password=str(password), salt_length=8, method='scrypt')
    if request.method == 'POST':
        name=request.form.get('name')
        with app.app_context():
            new_user = User(name=request.form.get('name'), email=request.form.get('email'), password=pass_scry)
            db.session.add(new_user)
            db.session.commit()
        return render_template('index.html', name=name)

    return render_template("register.html")


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        #colect data
        email = request.form.get('email')
        password = request.form.get('password')
        #find user by email
        with app.app_context():
            user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
        # user = User.query.filter_by(email=email).first()
        #
        # if user and check_password_hash(user.password, password):
        #     login_user(user)
            return render_template('secrets.html',name= user.name)
        else:
            flash('This email not exist, Please try again')
            return render_template("login.html")
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():

    return render_template("secrets.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', path='files/cheat_sheet.pdf')

if __name__ == "__main__":
    app.run(debug=True)
