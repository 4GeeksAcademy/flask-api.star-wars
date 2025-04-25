import os
from flask_admin import Admin
from models import db, User, People, Planet, Favorite 
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    admin = Admin(app, name='SWAPI Clone', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Favorite, db.session))