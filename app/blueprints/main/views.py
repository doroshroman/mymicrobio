from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
@main.route('/index')
def show_main_page():
	return render_template('main/index.html')

@main.route('/bio')
def show_bio():
    return render_template('main/bio.html')

@main.route('/hobbies')
def show_hobbies():
    return render_template('main/hobbies.html')