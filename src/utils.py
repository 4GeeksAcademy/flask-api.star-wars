from flask import jsonify, url_for, Blueprint, jsonify, request
from models import db, User, People, Planet, Favorite

api = Blueprint('api', __name__)

@api.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in people]), 200

@api.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get_or_404(people_id)
    return jsonify({'id': person.id, 'name': person.name}), 200

@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in planets]), 200

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify({'id': planet.id, 'name': planet.name}), 200

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users]), 200

@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.first()
    favorites = Favorite.query.filter_by(user_id=user.id).all()
    result = []
    for f in favorites:
        if f.people_id:
            result.append({'type': 'people', 'id': f.people_id})
        if f.planet_id:
            result.append({'type': 'planet', 'id': f.planet_id})
    return jsonify(result), 200

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.first()
    favorite = Favorite(user_id=user.id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorite planet added'}), 201

@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user = User.query.first()
    favorite = Favorite(user_id=user.id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorite people added'}), 201

@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user = User.query.first()
    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first_or_404()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorite planet deleted'}), 200

@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user = User.query.first()
    favorite = Favorite.query.filter_by(user_id=user.id, people_id=people_id).first_or_404()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorite people deleted'}), 200


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg' />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your proyect by following the <a href="https://start.4geeksacademy.com/starters/flask" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"
