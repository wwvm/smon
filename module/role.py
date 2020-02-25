from flask_restx import Resource, fields, Namespace
from smon_app import base, ma, db

Role = base.classes.smon_role
class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role

# role
api = Namespace('role', description='Role operations')
role = api.model('Role', {
    'id': fields.Integer(readonly=True, description='The role unique identifier'),
    'name' : fields.String(required=True, description=''),
    'scope' : fields.String(required=True, description=''),
    'remark' : fields.String(required=False, description='')
})

@api.route('/')
class RoleList(Resource):
    @api.marshal_list_with(role)
    def get(self):
        return RoleSchema(many=True).dump(db.session.query(Role).all())

    @api.expect(role)
    @api.marshal_with(role, code=201)
    def post(self):
        role = Role()
        role.name = api.payload['name']
        role.scope = api.payload['scope']
        role.remark = api.payload['remark']
        db.session.add(role)
        db.session.commit()
        return role, 201

@api.route('/<int:id>')
@api.response(404, 'Role not found')
@api.param('id', 'The role identifier')
class RoleDetail(Resource):
    @api.marshal_with(role)
    def get(self, id):
        return RoleSchema().dump(db.session.query(Role).filter_by(id=id).first())

    @api.response(204, 'Role deleted')
    def delete(self, id):
        role = db.session.query(Role).filter_by(id=id).first()
        db.session.delete(role)
        db.session.commit()
        return '', 204

    @api.expect(role)
    @api.marshal_with(role)
    def put(self, id):
        role = db.session.query(Role).filter_by(id=id).first()
        role.name = api.payload['name']
        role.scope = api.payload['scope']
        role.remark = api.payload['remark']
        db.session.commit()
        return RoleSchema().dump(role)
 
