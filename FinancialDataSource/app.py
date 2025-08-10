from flask import Flask
from controllers.b3_controller import b3_blueprint
from controllers.cdi_controller import cdi_blueprint
from controllers.selic_controller import selic_blueprint
from data.create_db import setup_database

app = Flask(__name__)

# à nossa aplicação principal.
app.register_blueprint(b3_blueprint, url_prefix='/b3')
app.register_blueprint(cdi_blueprint, url_prefix='/cdi')
app.register_blueprint(selic_blueprint, url_prefix='/selic')


if __name__ == '__main__':
    setup_database()
    app.run(debug=True)