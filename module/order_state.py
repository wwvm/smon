from flask_restx import Resource, fields, Namespace
from smon_app import base, ma, db

OrderState = base.classes.smon_order_state
class OrderStateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderState

# orderState
api = Namespace('orderState', description='OrderState operations')
orderState = api.model('OrderState', {
    'id': fields.Integer(readonly=True, description='The orderState unique identifier'),
    'order_id' : fields.Integer(required=True, description=''),
    'user_id' : fields.Integer(required=True, description=''),
    'user_name' : fields.String(required=True, description=''),
    'content' : fields.String(required=True, description='')
})

@api.route('/')
class OrderStateList(Resource):
    @api.marshal_list_with(orderState)
    def get(self):
        return OrderStateSchema(many=True).dump(db.session.query(OrderState).all())

    @api.expect(orderState)
    @api.marshal_with(orderState, code=201)
    def post(self):
        orderState = OrderState()
        orderState.order_id = api.payload['order_id']
        orderState.user_id = api.payload['user_id']
        orderState.user_name = api.payload['user_name']
        orderState.content = api.payload['content']
        db.session.add(orderState)
        db.session.commit()
        return orderState, 201

@api.route('/<int:id>')
@api.response(404, 'OrderState not found')
@api.param('id', 'The orderState identifier')
class OrderStateDetail(Resource):
    @api.marshal_with(orderState)
    def get(self, id):
        return OrderStateSchema().dump(db.session.query(OrderState).filter_by(id=id).first())

    @api.response(204, 'OrderState deleted')
    def delete(self, id):
        orderState = db.session.query(OrderState).filter_by(id=id).first()
        db.session.delete(orderState)
        db.session.commit()
        return '', 204

    @api.expect(orderState)
    @api.marshal_with(orderState)
    def put(self, id):
        orderState = db.session.query(OrderState).filter_by(id=id).first()
        orderState.order_id = api.payload['order_id']
        orderState.user_id = api.payload['user_id']
        orderState.user_name = api.payload['user_name']
        orderState.content = api.payload['content']
        db.session.commit()
        return OrderStateSchema().dump(orderState)
 
