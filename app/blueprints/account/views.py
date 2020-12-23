from flask import Blueprint, request, url_for, render_template
from flask_login import current_user, login_required 
from app.forms import UpdateAccountForm
import os


ab = Blueprint('account', __name__, template_folder='templates')

@ab.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file 
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        form.password.data = current_user.password_hash

    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account/account.html', title='Account', image=image_file, form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    name, ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (120, 120)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn