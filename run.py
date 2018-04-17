from application import *
from application.docs.views import docs

# Register the blueprints
app.register_blueprint(book)
app.register_blueprint(user)
app.register_blueprint(auth)
app.register_blueprint(docs)

if __name__ == '__main__':
    app_config('default')
    db.create_all()
    app.run(debug=True)
