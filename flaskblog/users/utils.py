import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


"""
    save_picture() takes in jpg or png for resize and saving:
        get random_hex for naming of the new-resized picture
        get the extension of the picture passed to function -> png/jpg
        combine random hex with file_ext for renaming and saving
        create picture_path that possess correct file path for picture
            -> Path to current flaskblog project, then static/profile_pics
        Read comments below for resizing schem
"""
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    #use '_' for total throwaway variable -> only want file_extension
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    """
        output_size is a tuple holding (dimensions of the new thumbnail)
        i object is set to the form.picture from the form UpdateAccountForm()
        use PIL(pillow) to craft thumbnail of the image using the size tuple
        save resized image using picture_path
    """
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    #return picture to Update account function save orignal picture
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                   sender='patricksheehancs@gmail.com',
                   recipients=[user.email])
    #_external=True discussed at 33:15 Episode:10
    msg.body = f'''To reset you password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)
