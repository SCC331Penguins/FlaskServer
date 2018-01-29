from flask import Flask

from Blueprints.post import post
from Blueprints.get import get

app = Flask(__name__)

app.register_blueprint(post)
app.register_blueprint(get)

app.config.from_pyfile('config.py')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)