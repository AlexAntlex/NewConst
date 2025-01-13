import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Z{jxeVyjujLtytuGhbvthyj1234'
    UPLOAD_FOLDER_USER = 'static/users_files/'