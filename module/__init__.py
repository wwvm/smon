from flask_restx import Api
from .position import api as position_api
from .section import api as section_api

api = Api(title='API', version='1.0')

api.add_namespace(position_api)
api.add_namespace(section_api)

