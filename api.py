from crypt import methods
from enum import unique
from re import X
from urllib.parse import quote_plus
from flask import Flask, abort, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, null


app = Flask(__name__)

password = quote_plus('emmanuel')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{}@localhost:5432/api_plantes'.format(
    password)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


########################################################################################
#
#                                  Classe Plante
#
########################################################################################
class Plant(db.Model):
    __tablename__ = 'plantes'

    id = db.Column(db.Integer, primary_key=True)
    ewe_name = db.Column(db.String(50), unique=True, nullable=False)
    french_name = db.Column(db.String(50), nullable=True)
    scientific_name = db.Column(db.String(50), unique=True, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'ewe_name': self.ewe_name,
            'scientific_name': self.scientific_name,
            'french_name': self.french_name
        }

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


db.create_all()


########################################################################################
#
#                                  route /
#
########################################################################################
@app.route('/')
def get_all_html():
    all = Plant.query.all()

    return render_template('plants.html', data=all)


########################################################################################
#
#                                  route /add
#
########################################################################################
@app.route('/add', methods=['POST', 'GET'])
def add_from_form():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        ewe = request.form.get('ewe_name')
        french = request.form.get('french_name', None)
        sci = request.form.get('sci_name')

        plant = Plant(ewe_name=ewe, french_name=french, scientific_name=sci)
        plant.create()

        return redirect(url_for('get_all_html'))


########################################################################################
#
#                                  route /create
#
########################################################################################
@app.route('/create')
def create():
    return render_template('create.html')


'''
API's endpoints

GET /plants (get all plants that are in the database)
GET /plants/id (get the plant that have the specific id)
POST /plants (create a new plant)
PATCH /plant/id (Modify an existing plant)
DELETE /plants/id (delete the plant that have the specific id)
'''

########################################################################################
#
#                            Endpoint GET /plants
#
########################################################################################


@app.route('/plants')
def get_all_json():
    return jsonify({
        'success': True,
        'total': Plant.query.count(),
        'Plants': [plant.format() for plant in Plant.query.all()]
    })


########################################################################################
#
#                            Endpoint GET /plants/id
#
########################################################################################
@app.route('/plants/<int:id>')
def get_specific(id):
    plant = Plant.query.get(id)

    if plant is None:
        abort(404)
    else:
        return jsonify({
            'id': id,
            'succes': True,
            'plant': plant.format()
        })


########################################################################################
#
#                            Endpoint POST /plants
#
########################################################################################
@app.route('/plants', methods=['POST'])
def add_from_json():
    body = request.get_json()
    ewe = body.get('ewe_name')
    french = body.get('french_name', None)
    sci = body.get('sci_name')

    plant = Plant(ewe_name=ewe, french_name=french, scientific_name=sci)
    plant.create()

    return jsonify({
        'success': True,
        'total': Plant.query.count(),
        'Plants': [pt.format() for pt in Plant.query.all()]
    })


########################################################################################
#
#                            Endpoint PATCH /plants/id
#
########################################################################################
@app.route('/plants/<int:id>', methods=['PATCH'])
def modify_from_json(id):
    plant = Plant.query.get(id)

    if plant is None:
        abort(404)
    else:
        body = request.get_json()
        ewe = body.get('ewe_name')
        french = body.get('french_name', None)
        sci = body.get('sci_name')

        plant = Plant.query.get(id)
        plant.ewe_name = ewe
        plant.scientific_name = sci
        plant.french_name = french
        plant.update()

        return jsonify({
            'success': True,
            'id': id,
            'Plants': plant.format()
        })




########################################################################################
#
#                         Endpoint DELETE /plants/<int:id> 
#
########################################################################################
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)

    if plant is None:
        abort(404)
    else:
        plant.delete()
        return jsonify({
            'success' : True,
            'id' : id,
            'etudiant' : plant.format(),
            'total_etudiants' : Plant.query.count()
        })


########################################################################################
#
#               THE API'S ERROR HANDLERS : THE RETURN ERRORS ON JSON FORMAT 
#
########################################################################################

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success" : False,
        "error" : 404,
        "message" : "Not Found"
    }), 404

@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "success" : False,
        "error" : 500,
        "message" : "Internal Server Error"
    }), 500


@app.errorhandler(400)
def not_found(error):
    return jsonify({
        "success" : False,
        "error" : 400,
        "message" : "Bad Request"
    }), 400


@app.errorhandler(403)
def not_found(error):
    return jsonify({
        "success" : False,
        "error" : 403,
        "message" : "Forbiden"
    }), 403


@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "success" : False,
        "error" : 405,
        "message" : "Method Not Allowed"
    }), 405