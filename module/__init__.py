from flask_restx import Api
from .position import api as position_api
from .section import api as section_api
from .role import api as role_api
from .user import api as user_api
from .assets import api as assets_api
from .provider import api as provider_api

api = Api(title='API', version='1.0')

api.add_namespace(position_api)
api.add_namespace(section_api)
api.add_namespace(role_api)
api.add_namespace(user_api)
api.add_namespace(assets_api)
api.add_namespace(provider_api)

