import random
from xmlrpc.client import boolean

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/random')
def get_random():
    result = db.session.execute(db.select(Cafe))
    all_cafe = result.scalars().all()
    random_cafe = random.choice(all_cafe)
    #you can use this
    return jsonify(cafe={'id':random_cafe.id,
                    'name':random_cafe.name,
                    'map_url':random_cafe.map_url,
                    'img_url':random_cafe.img_url,
                   'location':random_cafe.location,
                   'seats':random_cafe.seats,
                  ' has_toilet':random_cafe.has_toilet,
                   'has_wifi':random_cafe.has_wifi,
                   'has_sockets':random_cafe.has_sockets,
                   'can_take_calls':random_cafe.can_take_calls,
                   'coffee_price':random_cafe.coffee_price,})


@app.route('/all')
def all_cafes():
    with app.app_context():
        result =  db.session.execute(db.select(Cafe))
        all_cafe = result.scalars().all()
        cafes = []
        for cafe in all_cafe:
            cafes.append({'id':cafe.id,
            'name':cafe.name,
            'map_url':cafe.map_url,
            'img_url':cafe.img_url,
            'location':cafe.location,
            'seats':cafe.seats,
            'has_toilet':cafe.has_toilet,
            'has_wifi':cafe.has_wifi,
            'has_sockets':cafe.has_sockets,
            'can_take_calls':cafe.can_take_calls,
            'coffee_price':cafe.coffee_price,
                   })

    return jsonify(cafe=cafes)

@app.route('/search', methods=['GET', 'POST'])
def search():
    loc=request.args.get("loc")
    with app.app_context():
        result = db.session.execute(db.select(Cafe).where(Cafe.location == loc))
        cafes_in_location = result.scalars().all()
        cafes = []
        for cafe in cafes_in_location:
            cafes.append({'id':cafe.id,
            'name':cafe.name,
            'map_url':cafe.map_url,
            'img_url':cafe.img_url,
            'location':cafe.location,
            'seats':cafe.seats,
            ' has_toilet':cafe.has_toilet,
            'has_wifi':cafe.has_wifi,
            'has_sockets':cafe.has_sockets,
            'can_take_calls':cafe.can_take_calls,
            'coffee_price':cafe.coffee_price,
                   })
    if cafes_in_location:
        return jsonify(cafe=cafes)
    else:
        return jsonify(error={"sorry":"We dont have a coffee in at location"})

@app.route('/add', methods=['GET', 'POST',])
def add():
    try:
        with app.app_context():
            new_cafe = Cafe(name=request.args.get('name')  ,map_url=request.args.get('map_url'),img_url=request.args.get('img_url'), location=request.args.get('location'), seats=request.args.get('seats'), has_toilet=boolean(request.args.get('has_toilet')), has_wifi=boolean(request.args.get('has_wifi')), has_sockets=boolean(request.args.get('has_sockets')), can_take_calls=boolean(request.args.get('can_take_calls')), coffee_price=request.args.get('coffee_price'))
            db.session.add(new_cafe)
            db.session.commit()
        return jsonify(response={'success': 'you add a new cafe',})
    except:
        return jsonify(error={'error':'No item add in data base'})

@app.route('/update-coffee/<int:id>', methods=['PATCH','GET','POST'])
def patch(id):
    try:
        with app.app_context():
            coffee = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
            coffee.coffee_price = request.args.get('new_price')
            db.session.commit()
            return jsonify(success={'success':'you update the coffee price'})
    except:
        return jsonify(error={'sorry':'id dont found'})

@app.route('/report-closed/<int:id>', methods=['POST','GET','PATCH','DELETE'])
def delete(id):
    if request.args.get('api_key') == 'TopSecretAPIKey':
        try:
            with app.app_context():
                result = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
                db.session.delete(result)
                db.session.commit()
                return jsonify(success={'success':'coffee closed'})
        except:
            return jsonify(error={'error':'id not found'})
    else:
        return jsonify(error={'error':'API key dont matched'})




# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
