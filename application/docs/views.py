from flask import Blueprint, render_template

docs = Blueprint('docs', __name__, static_folder='static', template_folder = 'templates')

@docs.route('/docs')
def index():
	"Show an index template"

	return render_template('index.html')