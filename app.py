import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request
)
from flask_sqlalchemy import SQLAlchemy

from data_models import db, Author, Book


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)
# Damit wird die Flask-App mit dem Flask-SQLAlchemy-Code verbunden.
db.init_app(app)


@app.route('/')
def index():
    return render_template('home.html', title='Home')


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Fügt einen neuen Author zur Datenbank hinzu.
    Bei einem GET-Request wird das Formular angezeigt.
    Bei einem POST-Request werden die Formulardaten gespeichert
    und eine Erfolgsmeldung angezeigt.

    :return: Rendert das Formular mit oder ohne Erfolgsmeldung.
    """
    if request.method == 'GET':
        return render_template('add_author.html')

    else:
        author = Author(
            name=request.form["name"],
            birth_date=datetime.strptime(
                request.form["birth_date"], "%Y-%m-%d"
            ).date(),
            date_of_death=(
                datetime.strptime(
                    request.form["date_of_death"], "%Y-%m-%d"
                ).date()
                if request.form["date_of_death"]
                else None
            )
        )
        db.session.add(author)
        db.session.commit()

        return render_template(
            "add_author.html",
            success_message="Autor erfolgreich hinzugefügt!"
        )


# with app.app_context():
#     db.create_all()


if __name__ == "__main__":
    app.run(debug=True)