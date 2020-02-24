from flask_restx import Resource, fields, Namespace
from smon_app import base, ma, db

Section = base.classes.smon_section
class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section

# section
api = Namespace('section', description='Section operations')
section = api.model('Section', {
    'id': fields.Integer(readonly=True, description='The section unique identifier'),
    'section' : fields.String(required=True, description=''),
    'contact' : fields.String(required=True, description=''),
    'remark' : fields.String(required=False, description='')
})

@api.route('/')
class SectionList(Resource):
    @api.marshal_list_with(section)
    def get(self):
        return SectionSchema(many=True).dump(db.session.query(Section).all())

    @api.expect(section)
    @api.marshal_with(section, code=201)
    def post(self):
        section = Section()
        section.section = api.payload['section']
        section.contact = api.payload['contact']
        section.remark = api.payload['remark']
        db.session.add(section)
        db.session.commit()
        return section, 201

@api.route('/<int:id>')
@api.response(404, 'Section not found')
@api.param('id', 'The section identifier')
class SectionDetail(Resource):
    @api.marshal_with(section)
    def get(self, id):
        return SectionSchema().dump(db.session.query(Section).filter_by(id=id).first())

    @api.response(204, 'Section deleted')
    def delete(self, id):
        section = db.session.query(Section).filter_by(id=id).first()
        db.session.delete(section)
        db.session.commit()
        return '', 204

    @api.expect(section)
    @api.marshal_with(section)
    def put(self, id):
        section = db.session.query(Section).filter_by(id=id).first()
        section.section = api.payload['section']
        section.contact = api.payload['contact']
        section.remark = api.payload['remark']
        db.session.commit()
        return SectionSchema().dump(section)
 
