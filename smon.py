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

Position = Base.classes.smon_position
class PositionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Position

# building
p_ns = api.namespace('position', description='Position operations')
position = api.model('Position', {
    'id': fields.Integer(readonly=True, description='The position unique identifier'),
    'building' : fields.String(required=True, description=''),
    'floor' : fields.String(required=True, description=''),
    'room' : fields.String(required=False, description='')
})

@p_ns.route('/')
class PositionList(Resource):
    @p_ns.marshal_list_with(position)
    def get(self):
        return PositionSchema(many=True).dump(db.session.query(Position).all())

    @p_ns.expect(position)
    @p_ns.marshal_with(position, code=201)
    def post(self):
        position = Position()
        position.building = api.payload['building']
        position.floor = api.payload['floor']
        position.room = api.payload['room']
        db.session.add(position)
        db.session.commit()
        return position, 201

@p_ns.route('/<int:id>')
@p_ns.response(404, 'Position not found')
@p_ns.param('id', 'The position identifier')
class PositionDetail(Resource):
    @p_ns.marshal_with(position)
    def get(self, id):
        return PositionSchema().dump(db.session.query(Position).filter_by(id=id).first())

    @p_ns.response(204, 'Position deleted')
    def delete(self, id):
        position = db.session.query(Position).filter_by(id=id).first()
        db.session.delete(position)
        db.session.commit()
        return '', 204

    @p_ns.expect(position)
    @p_ns.marshal_with(position)
    def put(self, id):
        position = db.session.query(Position).filter_by(id=id).first()
        position.building = api.payload['building']
        position.floor = api.payload['floor']
        position.room = api.payload['room']
        db.session.commit()
        return PositionSchema().dump(position)
        
#db.session.close()


if __name__ == '__main__':
    app.run(debug=True)
