from flask_restx import Resource, fields, Namespace
from smon_app import base, ma, db

Assets = base.classes.smon_assets
class AssetsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Assets

# assets
api = Namespace('assets', description='Assets operations')
assets = api.model('Assets', {
    'id': fields.Integer(readonly=True, description='The assets unique identifier'),
    'name': fields.String(required=True, description=''),
    'breed' : fields.String(required=True, description=''),
    'brand' : fields.String(required=True, description=''),
    'serial' : fields.String(required=False, description=''),
    'warr_from' : fields.Date(required=True, description=''),
    'warr_end' : fields.Date(required=True, description=''),
    'warranty' : fields.String(required=True, description=''),
    'alloc_addr' : fields.String(required=False, description=''),
    'sign_date' : fields.Date(required=False, description=''),
    'section' : fields.String(required=False, description=''),
    'state' : fields.String(required=False, description=''),
    'remark' : fields.String(required=False, description='')
})

@api.route('/')
class AssetsList(Resource):
    @api.marshal_list_with(assets)
    def get(self):
        return AssetsSchema(many=True).dump(db.session.query(Assets).all())

    @api.expect(assets)
    @api.marshal_with(assets, code=201)
    def post(self):
        assets = Assets()
        assets.name = api.payload['name']
        assets.breed = api.payload['breed']
        assets.brand = api.payload['brand']
        assets.serial = api.payload['serial']
        assets.warr_from = api.payload['warr_from']
        assets.warr_end = api.payload['warr_end']
        assets.warranty = api.payload['warranty']
        assets.alloc_addr = api.payload['alloc_addr']
        assets.sign_date = api.payload['sign_date']
        assets.section = api.payload['section']
        assets.state = api.payload['state']
        assets.remark = api.payload['remark']
        db.session.add(assets)
        db.session.commit()
        return assets, 201

@api.route('/<int:id>')
@api.response(404, 'Assets not found')
@api.param('id', 'The assets identifier')
class AssetsDetail(Resource):
    @api.marshal_with(assets)
    def get(self, id):
        return AssetsSchema().dump(db.session.query(Assets).filter_by(id=id).first())

    @api.response(204, 'Assets deleted')
    def delete(self, id):
        assets = db.session.query(Assets).filter_by(id=id).first()
        db.session.delete(assets)
        db.session.commit()
        return '', 204

    @api.expect(assets)
    @api.marshal_with(assets)
    def put(self, id):
        assets = db.session.query(Assets).filter_by(id=id).first()
        assets.name = api.payload['name']
        assets.breed = api.payload['breed']
        assets.brand = api.payload['brand']
        assets.serial = api.payload['serial']
        assets.warr_from = api.payload['warr_from']
        assets.warr_end = api.payload['warr_end']
        assets.warranty = api.payload['warranty']
        assets.alloc_addr = api.payload['alloc_addr']
        assets.sign_date = api.payload['sign_date']
        assets.section = api.payload['section']
        assets.state = api.payload['state']
        assets.remark = api.payload['remark']
        db.session.commit()
        return AssetsSchema().dump(assets)
 
