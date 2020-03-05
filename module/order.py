from flask_restx import Resource, fields, Namespace
from smon_app import base, ma, db

Order = base.classes.smon_order
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

# order
api = Namespace('order', description='Order operations')
order = api.model('Order', {
    'id': fields.Integer(readonly=True, description='The order unique identifier'),
    'name' : fields.String(required=True, description=''),
    'state' : fields.String(required=True, description=''),
    'timeout' : fields.Integer(readonly=True, description=''),
    'content' : fields.String(required=True, description=''),
    'assets_id' : fields.Integer(required=True, description=''),
    'assets' : fields.String(required=True, description=''),
    'level' : fields.String(required=True, description=''),
    'section_id' : fields.Integer(required=True, description=''),
    'section' : fields.String(required=True, description=''),
    'building' : fields.String(required=True, description=''),
    'floor' : fields.String(required=True, description=''),
    'room' : fields.String(required=True, description=''),
    'user_id' : fields.Integer(readonly=True, description=''),
    'user_name' : fields.String(readonly=True, description=''),
    'report' : fields.DateTime(readonly=True, description=''),
    'contact' : fields.String(required=True, description=''),
    'phone' : fields.String(required=True, description=''),
    'source' : fields.String(required=True, description=''),
    'assign' : fields.DateTime(readonly=True, description=''),
    'accept' : fields.DateTime(readonly=True, description=''),
    'worker_id' : fields.Integer(required=False, description=''),
    'worker' : fields.String(required=False, description=''),
    'stars' : fields.Integer(required=False, description=''),
    'comment' : fields.String(required=False, description=''),
    'annex' : fields.String(required=False, description=''),
    'remark' : fields.String(required=False, description='')
})

@api.route('/')
class OrderList(Resource):
    @api.marshal_list_with(order)
    def get(self):
        return OrderSchema(many=True).dump(db.session.query(Order).all())

    @api.expect(order)
    @api.marshal_with(order, code=201)
    def post(self):
        order = Order()
        order.state = api.payload['state']
        order.content = api.payload['content']
        order.assets_id = api.payload['assets_id']
        order.assets = api.payload['assets']
        order.level = api.payload['level']
        order.section_id = api.payload['section_id']
        order.section = api.payload['section']
        order.building = api.payload['building']
        order.floor = api.payload['floor']
        order.room = api.payload['room']
        order.user_id = api.payload['user_id']
        order.user_name = api.payload['user_name']
        order.contact = api.payload['contact']
        order.phone = api.payload['phone']
        order.source = api.payload['source']
        order.assign = api.payload['assign']
        order.accept = api.payload['accept']
        order.worker_id = api.payload['worker_id']
        order.worker = api.payload['worker']
        order.stars = api.payload['stars']
        order.comment = api.payload['comment']
        order.annex = api.payload['annex']
        db.session.add(order)
        db.session.commit()
        return order, 201

@api.route('/<int:id>')
@api.response(404, 'Order not found')
@api.param('id', 'The order identifier')
class OrderDetail(Resource):
    @api.marshal_with(order)
    def get(self, id):
        return OrderSchema().dump(db.session.query(Order).filter_by(id=id).first())

    @api.response(204, 'Order deleted')
    def delete(self, id):
        order = db.session.query(Order).filter_by(id=id).first()
        db.session.delete(order)
        db.session.commit()
        return '', 204

    @api.expect(order)
    @api.marshal_with(order)
    def put(self, id):
        order = db.session.query(Order).filter_by(id=id).first()
        order.state = api.payload['state']
        order.content = api.payload['content']
        order.assets_id = api.payload['assets_id']
        order.assets = api.payload['assets']
        order.level = api.payload['level']
        order.section_id = api.payload['section_id']
        order.section = api.payload['section']
        order.building = api.payload['building']
        order.floor = api.payload['floor']
        order.room = api.payload['room']
        order.user_id = api.payload['user_id']
        order.user_name = api.payload['user_name']
        order.contact = api.payload['contact']
        order.phone = api.payload['phone']
        order.source = api.payload['source']
        order.assign = api.payload['assign']
        order.accept = api.payload['accept']
        order.worker_id = api.payload['worker_id']
        order.worker = api.payload['worker']
        order.stars = api.payload['stars']
        order.comment = api.payload['comment']
        order.annex = api.payload['annex']
        db.session.commit()
        return OrderSchema().dump(order)
 
