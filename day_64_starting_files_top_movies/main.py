from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from api_data import CollectMovies, CollectImage
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB---------------------
class Base(DeclarativeBase):
    pass
# Init the object
db = SQLAlchemy(model_class=Base)

# Configure the SQLite database, relative to de app instance
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-movies-collection.db"

# Initialize the flask app with the extension
db.init_app(app)

# CREATE TABLE------------------
# Creating rows of table
class Movies(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(259), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url:Mapped[str] = mapped_column(String(500), nullable=False)

# Creating the TABLE in DATABASE
try:
    with app.app_context():
        db.create_all()
except:
    pass

class MyForm(FlaskForm):
    rating = StringField(label='Rating', validators=[DataRequired()])
    review = StringField(label='Review', validators=[DataRequired()])
    submit = SubmitField(label='Update')

class AddForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired()])
    submit = SubmitField(label='Done')

# ----------------  Recording the first data
# with app.app_context():
#     new_movie = Movies(title="Avatar The Way of Water", year=2022, description='Set more than a decade after the '
#                                                                                'events of the first film, '
#                                                                                'learn the story of the Sully family ('
#                                                                                'Jake, Neytiri, and their kids), '
#                                                                                'the trouble that follows them, '
#                                                                                'the lengths they go to keep each '
#                                                                                'other safe, the battles they fight to '
#                                                                                'stay alive, and the tragedies they '
#                                                                                'endure.', rating=7.3, ranking=9,
#                        review="MI liked the water.",
#                        img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg")
#     db.session.add(new_movie)
#     db.session.commit()

@app.route("/")
def home():
    all_movies = None
    with app.app_context():
        movies = db.session.execute(db.select(Movies).order_by(Movies.rating)).scalars()
        all_movies = movies.all()
    return render_template("index.html", all_movies= all_movies)

@app.route('/edit/<id>')
def edit(id):
    id = id
    my_form = MyForm()
    print(f"{my_form.review.data}, {my_form.review.data}")
    return render_template('edit.html', form=my_form, id=id)

@app.route('/update/<id>', methods=['GET','POST'])
def update(id):
    form = MyForm()
    id = id
    with app.app_context():
        movie = db.session.execute(db.select(Movies).where(Movies.id == id)).scalar()
        movie.rating = float(request.args.get("rating"))
        movie.review = request.args.get("review")
        db.session.commit()
    print(f'it will update this id: {id}')
    return redirect('/')


@app.route('/delete/<id>')
def  delete(id):
    id = id
    with app.app_context():
        movie = db.session.execute(db.select(Movies).where(Movies.id == id)).scalar()
        db.session.delete(movie)
        db.session.commit()
    return redirect('/')

@app.route('/add')
def add_title():
    form = AddForm()

    return render_template('add.html', form=form)

@app.route('/add_title', methods=['GET', 'POST'])
def add_collect():
    title = request.args.get('title')
    movies = CollectMovies(title)
    title_movies = movies.collect()
    return render_template('select.html', titles=title_movies)

@app.route('/show_movie/<id>/<title>')
def show(id,title):
    id = id
    title = title
    obj_img = CollectImage(int(id))
    img = obj_img.collect()
    movie = CollectMovies(title)
    data = movie.collect()
    datas = movie.found_movie_by_id(int(id))
    print(datas[0]['title'])
    with app.app_context():
        new_movie = Movies(title=datas[0]['title'], year=datas[0]['date'], description=datas[0]['overview'], rating=0, ranking=0,
                           review=0,
                           img_url=f"https://image.tmdb.org/t/p/w500{img}")
        db.session.add(new_movie)
        db.session.commit()
    with app.app_context():
        movie = db.session.execute(db.select(Movies).where(Movies.title == datas[0]['title'] )).scalar()
    return redirect(url_for('edit', id= movie.id))

if __name__ == "__main__":
    app.run(debug=True)
