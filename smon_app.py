from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config.from_pyfile('smon.cfg')

# init db
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)

# load db
base = automap_base()
base.prepare(db.engine, reflect=True)

if __name__ == '__main__':
    from module import api
    api.init_app(app)
    app.run(debug=True)
    print('exiting ...')
    db.session.close()
