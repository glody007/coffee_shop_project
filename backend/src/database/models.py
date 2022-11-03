import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    recycler = Recycler(
        title='Demo',
        position='Salama'
    )


    recycler.insert()
# ROUTES

'''
Recycler
a persistent recycler entity, extends the base SQLAlchemy Model
'''


class Recycler(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # String position
    position = Column(String(180), nullable=False)

    '''
    short()
        short form representation of the Recycler model
    '''

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'position': self.position
        }

    '''
    long()
        long form representation of the Recycler model
    '''

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'position': self.position
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            recycler = Recycler(title=req_title, recipe=req_recipe)
            recycler.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            recycler = Recycler(title=req_title, recipe=req_recipe)
            recycler.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            recycler = Recycler.query.filter(Recycler.id == id).one_or_none()
            recycler.title = 'Black Coffee'
            recycler.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
