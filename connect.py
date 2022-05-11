import os
DEBUG = True
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/movie_demo'
SQLALCHEMY_TRACK_MODIFICATIONS = False

