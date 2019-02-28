import os


basedir = os.path.abspath(os.path.dirname(__file__))

POSTGREDB = {
    'HOST' : 'localhost',
    'PORT' : 5432,
    'USERNAME' : 'aloha',
    'PASSWORD' : 'aloha_pass',
    'DATABASE' : 'users',
    'PATTERN' : 'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
}

SQLITEDB = 'sqlite:///' + os.path.join(basedir, 'auth.db')