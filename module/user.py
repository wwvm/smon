from flask_restx import Resource, fields, Namespace
from smon_app import base, ma, db

User = base.classes.smon_user
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# user
api = Namespace('user', description='User operations')
user = api.model('User', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'name' : fields.String(required=True, description=''),
    'scope' : fields.String(required=True, description=''),
    'section' : fields.String(required=True, description=''),
    'position' : fields.String(required=False, description=''),
    'signin' : fields.String(required=True, description=''),
    'secret' : fields.String(required=True, description=''),
    'wechat' : fields.String(required=True, description=''),
    'role_id' : fields.Integer(required=True, description=''),
    'role_name' : fields.String(required=True, description=''),
    'labor' : fields.String(required=False, description=''),
    'phone' : fields.String(required=False, description=''),
    'speedy' : fields.String(required=False, description=''),
    'gender' : fields.String(required=True, description=''),
    'state' : fields.String(required=False, description='')
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user)
    def get(self):
        return UserSchema(many=True).dump(db.session.query(User).all())

    @api.expect(user)
    @api.marshal_with(user, code=201)
    def post(self):
        user = User()
        user.name = api.payload['name']
        user.scope = api.payload['scope']
        user.section = api.payload['section']
        user.position = api.payload['position']
        user.signin = api.payload['signin']
        user.secret = api.payload['secret']
        user.wechat = api.payload['wechat']
        user.role_id = api.payload['role_id']
        user.role_name = api.payload['role_name']
        user.labor = api.payload['labor']
        user.phone = api.payload['phone']
        user.speedy = api.payload['speedy']
        user.gender = api.payload['gender']
        user.state = api.payload['state']
        db.session.add(user)
        db.session.commit()
        return user, 201

@api.route('/<int:id>')
@api.response(404, 'User not found')
@api.param('id', 'The user identifier')
class UserDetail(Resource):
    @api.marshal_with(user)
    def get(self, id):
        return UserSchema().dump(db.session.query(User).filter_by(id=id).first())

    @api.response(204, 'User deleted')
    def delete(self, id):
        user = db.session.query(User).filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return '', 204

    @api.expect(user)
    @api.marshal_with(user)
    def put(self, id):
        user = db.session.query(User).filter_by(id=id).first()
        user.name = api.payload['name']
        user.scope = api.payload['scope']
        user.section = api.payload['section']
        user.position = api.payload['position']
        user.signin = api.payload['signin']
        user.secret = api.payload['secret']
        user.wechat = api.payload['wechat']
        user.role_id = api.payload['role_id']
        user.role_name = api.payload['role_name']
        user.labor = api.payload['labor']
        user.phone = api.payload['phone']
        user.speedy = api.payload['speedy']
        user.gender = api.payload['gender']
        db.session.commit()
        return UserSchema().dump(user)
 
