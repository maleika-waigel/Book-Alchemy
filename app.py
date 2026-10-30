import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request
)

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
    books = Book.query.all()
    authors = Author.query.all()
    return render_template('home.html', books=books, authors=authors)


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


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Fügt ein neues Buch zur Datenbank hinzu.
    Bei einem GET-Request wird das Formular mit den vorhandenen
    Autoren angezeigt.
    Bei einem POST-Request werden die Formulardaten gespeichert
    und eine Erfolgsmeldung angezeigt.

    :return: Rendert das Formular mit oder ohne Erfolgsmeldung.
    """
    if request.method == 'GET':
        authors = Author.query.all()
        return render_template('add_book.html', authors=authors)

    else:
        book = Book(
            isbn=request.form["isbn"],
            title=request.form["title"],
            publication_year=(
                int(request.form["publication_year"])
                if request.form["publication_year"]
                else None
            ),
            author_id=int(request.form["author_id"])
        )
        db.session.add(book)
        db.session.commit()

        authors = Author.query.all()

        return render_template(
            "add_book.html",
            success_message="Buch erfolgreich hinzugefügt!",
            authors=authors
        )


# with app.app_context():
#     db.create_all()


if __name__ == "__main__":
    app.run(debug=True)