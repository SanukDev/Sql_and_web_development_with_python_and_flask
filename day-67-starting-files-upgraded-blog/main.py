from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class MyForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    author = StringField(label='Author', validators=[DataRequired()])
    img_url =  StringField(label='Image URL', validators=[DataRequired()])
    body = CKEditorField(label='Body')
    submit = SubmitField(label='Done')

with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO:
    with app.app_context():
        result = db.session.execute(db.select(BlogPost)).scalars().all()
    posts = result
    return render_template("index.html", all_posts=posts)

# TODO:
@app.route('/post/<post_id>')
def show_post(post_id):
    post_id = post_id
    # TODO:
    with app.app_context():
        result = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id))
        requested_post = result.scalar()
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/add', methods=['POST', 'GET'])
def add_post():
    form = MyForm()
    if form.validate_on_submit():
        with app.app_context():
            blog = BlogPost(title=form.title.data, subtitle=form.subtitle.data, author=form.author.data, img_url=form.img_url.data,body=form.body.data, date='1910/12/09')
            db.session.add(blog)
            db.session.commit()
        return redirect('/')
    return render_template('make-post.html', form=form)

# @app.route('/add-post', methods=['POST', 'GET'])
# def add():
#     with app.app_context():
#         blog = BlogPost(title=request.args.get('title'), subtitle=request.args.get('subtitle'), author=request.args.get('author'), img_url=request.args.get('img_url'),body=request.args.get('body'), date='1910/12/09')
#         db.session.add(blog)
#         db.session.commit()
#     return redirect('/')
# TODO: edit_post() to change an existing blog post
@app.route('/edit-post/<id>', methods=['GET','POST'])
def edit_init(id):
    id = id
    boo = False
    result = db.session.execute(db.select(BlogPost).where(BlogPost.id == id))
    requested_post = result.scalar()
    form = MyForm(
        title = requested_post.title,
        subtitle = requested_post.subtitle,
        author = requested_post.author,
        img_url =  requested_post.img_url,
        body = requested_post.body
    )
    if form.validate_on_submit():
        boo = True
        requested_post.title = form.title.data
        requested_post.subtitle = form.subtitle.data
        requested_post.author = form.author.data
        requested_post.img_url = form.img_url.data
        requested_post.body = form.body.data
        print(f"{requested_post.title},relloooooo {form.title.data}")
        db.session.commit()
        return redirect(url_for('show_post', post_id= id))
    return render_template('make-post.html', id=id, form=form, boo= boo,is_edit=True)
# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
