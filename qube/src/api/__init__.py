# /usr/bin/python
"""
Add docstring here
"""

import os

from flask import Flask
from flask_cors import CORS
from flask_mongoalchemy import MongoAlchemy

app = Flask('kitten33')
CORS(app)
app.config['MONGOALCHEMY_CONNECTION_STRING'] = \
    os.getenv('KITTEN33_MONGOALCHEMY_CONNECTION_STRING', '')
app.config['MONGOALCHEMY_SERVER'] = \
    os.getenv('KITTEN33_MONGOALCHEMY_SERVER', '')
app.config['MONGOALCHEMY_PORT'] = \
    os.getenv('KITTEN33_MONGOALCHEMY_PORT', 0)
app.config['MONGOALCHEMY_DATABASE'] = \
    os.getenv('KITTEN33_MONGOALCHEMY_DATABASE', '')

persist_db = MongoAlchemy(app)
