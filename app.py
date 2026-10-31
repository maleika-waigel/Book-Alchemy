import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    abort,
    redirect,
    url_for
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
    """
    Zeigt die Bücher auf der Startseite an.
    Ermöglicht die Stichwortsuche und Sortierung nach Titel,
    Autorname oder Veröffentlichungsjahr.
    Zeigt nach dem Löschen eines Buches eine Erfolgsmeldung an.

    :return: Rendert die Startseite mit den gefilterten und
             sortierten Büchern sowie einer optionalen Erfolgsmeldung.
    """
    sort_by = request.args.get('sort', 'title')
    search = request.args.get('search', '').strip()
    success_message = None

    if request.args.get('deleted') == 'true':
        success_message = "Buch erfolgreich gelöscht!"

    query = Book.query

    if search:
        query = query.filter(Book.title.ilike(f'%{search}%'))

    if sort_by == 'author':
        query = query.join(Author).order_by(Author.name)
    elif sort_by == 'publication_year':
        query = query.order_by(Book.publication_year)
    else:
        query = query.order_by(Book.title)

    books = query.all()

    return render_template(
        'home.html',
        books=books,
        sort_by=sort_by,
        search=search,
        success_message=success_message
    )


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
        return render_template(
            'add_book.html',
            authors=authors
        )

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


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Löscht ein Buch aus der Datenbank anhand der ID.

    :param book_id: ID des zu löschenden Buches.
    :return: Leitet zur Startseite weiter.
    """
    book = db.session.get(Book, book_id)

    if book is None:
        abort(404)

    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('index', deleted='true'))


# with app.app_context():
#     db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=5002)