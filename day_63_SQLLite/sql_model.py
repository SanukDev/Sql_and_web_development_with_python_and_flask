from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm.sync import update


class Base(DeclarativeBase):
    pass

# Init the DB object
db = SQLAlchemy(model_class=Base)

# Create the flask app
app = Flask(__name__)

# Configure the SQLite database, relative to de app instance
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# Initialize the flask app with the extension
db.init_app(app)

#---------------------CREATE TABLE----------------------
# Creating the rows of the Table
class Books(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250),nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

# Creating a TABLE in database
# with app.app_context():
#     db.create_all()

#----------------------INSERT--------------------------
#add data in DATA BASE
# books_new = Books(id=1, title= "Harry Potter", author= "J.K. Rowling", rating='9.3')
# app.app_context().push()
# books_new = Books(title= "The Process", author= "Franz Kafka", rating='8.3')
# app.app_context().push()
# db.session.add(books_new)
# db.session.commit()

#------------------------READ-------------------------
with app.app_context():
    # Read all data in the row
    # result = db.session.execute(db.select(Books).order_by(Books.title))
    # all_books = result.scalars()
    # print(all_books)
    book = db.session.execute(db.select(Books).where(Books.id == 2)).scalar()
    print(book.title)

#------------------------UPDATE-------------------------
# with app.app_context():
#     update_books = db.session.execute(db.select(Books).where(Books.title == "Harry Potter")).scalar()
#     update_books.title = "Harry Potter and the Chamber of Secrets"
#     db.session.commit()

# Update a record by Primary Key
# book_id = 1
# with app.app_context():

#     or book_to_update = db.get_or_404(Book, book_id)

#     update_title = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
#     update_title.title = "Harry Potter and the Goblet of fire"
#     db.session.commit()

#--------------------------DELETE-----------------------------

book_id = 1
with app.app_context():
    update_book = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    db.session.delete(update_book)
    db.session.commit()