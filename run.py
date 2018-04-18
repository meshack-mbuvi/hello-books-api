from application import *


if __name__ == '__main__':
    app = app_config('staging')
    db.create_all()
    app.run(debug=True)
