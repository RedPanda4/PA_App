from flask import *
import datetime

app = Flask(__name__)


@app.template_filter()
def date(value):
	value = datetime.datetime.fromtimestamp(value/1000.0)
	return value.strftime('%Y-%m-%d')
