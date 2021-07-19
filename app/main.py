from app import app

import view
from projects.blueprint import projects

app.register_blueprint(projects, url_prefix='/projects')


if __name__ == '__main__':
    app.run()