# import sqlite3
from traceback import print_exc

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

#init  the DB object
db = SQLAlchemy(model_class=Base)

#creating the flask app
app = Flask(__name__)

#configure the SQLite database, relative to the app instance
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

#initialize the flask app with the extension
db.init_app(app)

##----------------CREATE TABLE----------------------
#creating rows of the TABLE
class Books(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

#creating the TABLE in database
try:
    with app.app_context():
        db.create_all()
except:
    pass


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Books).order_by(Books.title))
        all_books = result.scalars().all()
    for book in all_books:
        print(f"This is the title of the book {book.title}, {book.author}, {book.rating}")
    return render_template("index.html", all_books=all_books)

@app.route("/add")
def add():
    return render_template("add.html")
@app.route("/susses", methods=['POST'])
def susses():
    print(f"{request.form['title']}, {request.form['author']}, {request.form['rating']}")
    with app.app_context():
        new_book = Books(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()

    return redirect('/')

@app.route("/edit/<id>")
def edit(id):
    id = id
    with app.app_context():
        book = db.session.execute(db.select(Books).where(Books.id == id)).scalar()

    return render_template("edit_rating.html", book=book)

@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    new_rating = request.form['rating']
    with app.app_context():
        book = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
        book.rating = new_rating
        db.session.commit()
    print(f"update this {id}, {new_rating}")
    return redirect('/')


@app.route('/delete/<id>')
def delete(id):
    id = id

    with app.app_context():
        book = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
        db.session.delete(book)
        db.session.commit()
    print(id)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

print('hello broo')
#


# ----------INSERT DATA IN DATABASE
# with app.app_context():
#     new_book = Books(id=1, title='Harry Potter', author='J.K', rating=7.9)
#     db.session.add(new_book)
#     db.session.commit()

# -----------READ ALL DATA FROM THE DATABASE
# with app.app_context():
#     result = db.session.execute(db.select(Books).order_by(Books.title))
#     all_books = result.scalars().all()

# -----------READ A PARTICULAR DATA FROM THE DATABASE
# with app.app_context():
#     result = db.session.execute(db.select(Books).where(Books.title == 'Harry Potter'))
#     all_books = result.scalar()
#
# print(all_books)

# -----------UPDATE A PARTICULAR DATA IN DATABASE
# with app.app_context():
#     select_book = db.session.execute(db.select(Books).where(Books.title == "Harry Potter")).scalar()
#     select_book.title = "Harry Potter New Title"
#     db.session.commit()

#------------DELETE
# book_id = 1
# with app.app_context():
#     update_book = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
#     db.session.delete(update_book)
#     db.session.commit()




#conecting the database
# db = sqlite3.connect("books-collection.db")
#
# cursor = db.cursor()
# cursor.execute("""CREATE TABLE books (id INTEGER PRIMARY KEY,
#                   title VARCHAR(250 NOT NULL UNIQUE,
#                   autor VARCHAR(250) NOT NULL,
#                   rating FLOAT NOT NULL)""")
#
# cursor.execute("""INSERT INTO books VALUES (1, 'Harry Potter', 'J.K', 9)""")
# db.commit()