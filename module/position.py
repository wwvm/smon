from flask_restx import Resource, fields, Namespace
from smon_app import base, ma, db

Position = base.classes.smon_position
class PositionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Position

# position
api = Namespace('position', description='Position operations')
position = api.model('Position', {
    'id': fields.Integer(readonly=True, description='The position unique identifier'),
    'building' : fields.String(required=True, description=''),
    'floor' : fields.String(required=True, description=''),
    'room' : fields.String(required=False, description='')
})

@api.route('/')
class PositionList(Resource):
    @api.marshal_list_with(position)
    def get(self):
        return PositionSchema(many=True).dump(db.session.query(Position).all())

    @api.expect(position)
    @api.marshal_with(position, code=201)
    def post(self):
        position = Position()
        position.building = api.payload['building']
        position.floor = api.payload['floor']
        position.room = api.payload['room']
        db.session.add(position)
        db.session.commit()
        return position, 201

@api.route('/<int:id>')
@api.response(404, 'Position not found')
@api.param('id', 'The position identifier')
class PositionDetail(Resource):
    @api.marshal_with(position)
    def get(self, id):
        return PositionSchema().dump(db.session.query(Position).filter_by(id=id).first())

    @api.response(204, 'Position deleted')
    def delete(self, id):
        position = db.session.query(Position).filter_by(id=id).first()
        db.session.delete(position)
        db.session.commit()
        return '', 204

    @api.expect(position)
    @api.marshal_with(position)
    def put(self, id):
        position = db.session.query(Position).filter_by(id=id).first()
        position.building = api.payload['building']
        position.floor = api.payload['floor']
        position.room = api.payload['room']
        db.session.commit()
        return PositionSchema().dump(position)
 
