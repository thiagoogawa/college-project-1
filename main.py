from flask import Flask 
from route.home import home_routes
from route.user import user_routes 
from route.events import event_routes
from route.principal import principal

app = Flask(__name__)

# Agrupamento de rotas = blueprints
app.register_blueprint(home_routes)
app.register_blueprint(user_routes, url_prefix = '/users')
app.register_blueprint(event_routes, url_prefix = '/events')
app.register_blueprint(principal, url_prefix = '/')


app.run(debug=True)