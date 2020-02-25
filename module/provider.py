from flask_restx import Resource, fields, Namespace
from smon_app import base, ma, db

Provider = base.classes.smon_provider
class ProviderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Provider

# provider
api = Namespace('provider', description='Provider operations')
provider = api.model('Provider', {
    'id': fields.Integer(readonly=True, description='The provider unique identifier'),
    'name' : fields.String(required=True, description=''),
    'abbrev' : fields.String(required=True, description=''),
    'province' : fields.String(required=True, description=''),
    'city' : fields.String(required=True, description=''),
    'district' : fields.String(required=False, description=''),
    'address' : fields.String(required=True, description=''),
    'contact' : fields.String(required=True, description=''),
    'phone' : fields.String(required=True, description=''),
    'title' : fields.String(required=True, description=''),
    'email' : fields.String(required=True, description=''),
    'scope' : fields.String(required=True, description=''),
    'section' : fields.String(required=False, description=''),
    'sec_cont' : fields.String(required=False, description=''),
    'state' : fields.String(required=False, description='')
})

@api.route('/')
class ProviderList(Resource):
    @api.marshal_list_with(provider)
    def get(self):
        return ProviderSchema(many=True).dump(db.session.query(Provider).all())

    @api.expect(provider)
    @api.marshal_with(provider, code=201)
    def post(self):
        provider = Provider()
        provider.name = api.payload['name']
        provider.abbrev = api.payload['abbrev']
        provider.province = api.payload['province']
        provider.city = api.payload['city']
        provider.district = api.payload['district']
        provider.address = api.payload['address']
        provider.contact = api.payload['contact']
        provider.phone = api.payload['phone']
        provider.title = api.payload['title']
        provider.email = api.payload['email']
        provider.scope = api.payload['scope']
        provider.section = api.payload['section']
        provider.sec_cont = api.payload['sec_cont']
        provider.state = api.payload['state']
        db.session.add(provider)
        db.session.commit()
        return provider, 201

@api.route('/<int:id>')
@api.response(404, 'Provider not found')
@api.param('id', 'The provider identifier')
class ProviderDetail(Resource):
    @api.marshal_with(provider)
    def get(self, id):
        return ProviderSchema().dump(db.session.query(Provider).filter_by(id=id).first())

    @api.response(204, 'Provider deleted')
    def delete(self, id):
        provider = db.session.query(Provider).filter_by(id=id).first()
        db.session.delete(provider)
        db.session.commit()
        return '', 204

    @api.expect(provider)
    @api.marshal_with(provider)
    def put(self, id):
        provider = db.session.query(Provider).filter_by(id=id).first()
        provider.name = api.payload['name']
        provider.abbrev = api.payload['abbrev']
        provider.province = api.payload['province']
        provider.city = api.payload['city']
        provider.district = api.payload['district']
        provider.address = api.payload['address']
        provider.contact = api.payload['contact']
        provider.phone = api.payload['phone']
        provider.title = api.payload['title']
        provider.email = api.payload['email']
        provider.scope = api.payload['scope']
        provider.section = api.payload['section']
        provider.sec_cont = api.payload['sec_cont']
        provider.state = api.payload['state']
        db.session.commit()
        return ProviderSchema().dump(provider)
 
