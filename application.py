import base64
import urllib2
import urllib
import webbrowser

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/register_user')
def register_user():
    code = request.args.get("code")
    return 'Code: {0}'.format(code)


app.run(port=9090)

