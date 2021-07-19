
class Configuration:

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/flaskproject'
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    #
    # # === Flask security ===
    SECURITY_PASSWORD_SALT = 'supersalt'
    SECURYTY_PASSWORD_HASH = 'bcrypt'
    #
    ######## Flask-Mail #######
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'technicalandrew70@gmail.com'
    MAIL_DEFAULT_SENDER = 'technicalandrew70@gmail.com'
    MAIL_PASSWORD = 'd27m02Y1981'