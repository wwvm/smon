from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.automap import automap_base
from flask_restx import Api, Resource, fields

# init app
app = Flask(__name__)
app.config.from_pyfile('smon.cfg')
api = Api(app, version='1.0')

# init DB
db = SQLAlchemy(app)

# init Marshmallow
ma = Marshmallow(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

Nav = Base.classes.nav
class NavSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Nav

navs_schema = NavSchema(many=True)

@app.route('/nav')
def navs():
    return navs_schema.jsonify(db.session.query(Nav).all())

# --------------
#
# User mangement
#
User = Base.classes.user
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


@app.route('/api/users/<int:page>', methods=['GET'])
def get_users(page):
    return UserSchema(many=True).jsonify(db.session.query(User).all())

@app.route('/api/user/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.query(User).filter_by(id=id).first()
    if user is None:
        response = {'message': 'user does not exist'}
        return jsonify(response), 404
    return UserSchema().dump(user)

@app.route('/api/user')
def add_user():
    print(request)
# --------------
import module.position
#db.session.close()


if __name__ == '__main__':
    app.run(debug=True)
