from flask_restx import Resource, fields, Namespace
from smon_app import base, ma, db

Nav = base.classes.nav
class NavSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Nav

# nav
api = Namespace('nav', description='Nav operations')
nav = api.model('Nav', {
    'id': fields.Integer(readonly=True, description='The nav unique identifier'),
    'title' : fields.String(required=True, description=''),
    'url' : fields.String(required=True, description=''),
    'level' : fields.Integer(required=True, description=''),
    'parent' : fields.Integer(required=True, description='')
})

@api.route('/<int:page>')
class NavList(Resource):
    @api.marshal_list_with(nav)
    def get(self, page):
        datas = db.session.query(Nav).paginate(per_page=2,page=2,error_out=True)
        print(datas.items)
        return NavSchema(many=True).dump(datas.items)

    @api.expect(nav)
    @api.marshal_with(nav, code=201)
    def post(self):
        nav = Nav()
        nav.name = api.payload['name']
        nav.scope = api.payload['scope']
        nav.remark = api.payload['remark']
        db.session.add(nav)
        db.session.commit()
        return nav, 201

@api.route('/nav/<int:id>')
@api.response(404, 'Nav not found')
@api.param('id', 'The nav identifier')
class NavDetail(Resource):
    @api.marshal_with(nav)
    def get(self, id):
        return NavSchema().dump(db.session.query(Nav).filter_by(id=id).first())

    @api.response(204, 'Nav deleted')
    def delete(self, id):
        nav = db.session.query(Nav).filter_by(id=id).first()
        db.session.delete(nav)
        db.session.commit()
        return '', 204

    @api.expect(nav)
    @api.marshal_with(nav)
    def put(self, id):
        nav = db.session.query(Nav).filter_by(id=id).first()
        nav.name = api.payload['name']
        nav.scope = api.payload['scope']
        nav.remark = api.payload['remark']
        db.session.commit()
        return NavSchema().dump(nav)
 
