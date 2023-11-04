"""
Uruchomienie Linux:
export FLASK_APP=hello.py
flask run
Uruchomienie Windows:
set FLASK_APP=hello.py
$env:FLASK_APP = "hello.py"
flask run

Tryb debugowania Linux
export FLASK_DEBUG=1
Tryb debugowania Windows
set FLASK_DEBUG=1
$env:FLASK_DEBUG = "1"

Zamiast flask run można uruchomić programowo:
app = Flask(__name__)
if __name__=="__main__":
    app.run(debug=True)
    app.run()

-------------------------------------
Flask Podstawy
-------------------------------------
route           - trasa - powiązanie adresu z funkcją Pythona, która obsłuży dany adres.
                1 za pomocą dekoratora app.route("adres...")
                2 za pomocą funkcji app.add_url_rule("/", "index", index)
funckja widoku  - funkcja obsługująca dany adres URL, np index()
URL             - adresy oprócz częsci statycznej, zawierają część dynamiczną w ostrych nawiasach <>
                <data>
                <int:data>
kontekst        - pozwala na globalny dostęp do elementó Flask z poziomu wątku
                Zmienna             Kontekst                Opis
                current_app         kontekst aplikacji      instancja aktywnej aplikacji
                g                   kontekst aplikacji      obiekt pamięci tymczasowej, resetowane po każdym żądaniu
                request             kontekst żądania        obiekt z żądaniem zapytania
                session             kontekst żądania        sesja użytkownia - słownik z zapamiętanymi wartościami
                                                            między żądaniami
request         - obiekt żądania, zawiera informacje przesłane w żądaniu
response        - obiekt odpowiedzi tworzony przez make_response. Zawiera atrybuty pozwalające na
                zarządzanie odpowiedzią:
                status_code
                headers
                content_lenght
                content_type
                set_cookie()
                delete_cookie()
                set_data()
                get_data()
redirect        - przekierowanie - specjalny rodzaj odpowiedzi/response - nie posiada dokumentu strony, daje nowy URL
hooki           - powtarzalne funkcje wykonywane przed/po wysłaniu żądania, implementowane w postaci dekoratory
                before_request
                before_first_request
                after_request
                teardown_request
-------------------------------------
Szablony Jinja i Bootstrap
-------------------------------------
jinja           - mechanizm szablonów i renderowania. Jinja jest jednym z tych elementów flaska który pozwala oddzielić
                logikę prezentacji od logiki aplikacji. Fizycznie jest to plik zawierający text odpowiedzi.
                Renderowanei szblonów odbywa się za pomocą funkcji render_template.
                Domyślnie szablony szukane są w katalogu: templates
jinja {{}}      - zmienne umieszczone w szablonie. Moga być róźnego typu:
                {{ slownik["klucz"] }}
                {{ lista[element] }}
                {{ jakis_obiekt.metoda() }}
jinja filtry    - zmienne mogą podlegać modyfikacji poprzez filtry
                {{ zmienn|capitalize }} - wyświetla zmienną z pierwszym znakiem z dużej litery
                safe        - renderuje zawartosć bez interpretowania znaków modyfikacji
                capitalize  - pierwsza lotera duża
                lower       - same małe litery
                upper       - same duże litery
                title       - pierwsza litera każdego słowa duża
                trim        - usuwa białe znaki na początki i na końcu
                striptags   - przed renderowaniem usuwa wszystkie znaczniki HTML
jinja if        - struktury sterujące
                {% if data %}
                    Hello {{data}}, what's up?
                {% else %}
                    I do not know you :(
                {% endif %}
jinja for       - pętla
                <ul>
                    {% for item in lista %}
                        <li>{{item}}</li>
                    {% endfor %}
                </ul>
jinja macro     - makra pozwalają na definiowanie funkcji
                {% macro render_content(data) %}
                    <li>{{ data }}</li>
                {% endmacro %}

                <ul>
                    {% for item in contents %}
                        {{ render_content(item) }}
                    {% endfor %}
                </ul>
jinja import    - makra można przechowywać w osobnych plikach, a potem importować w ten sam sposób jak w Pythonie
                {% import "moje_makra.html" as makra %}
                <ul>
                    {% for item in elements %}
                        {{ makra.render_content(item) }}
                    {% endfor %}
                </ul>
jinja include   - pozwala na dołączenie części kodu
                {% include "common.html" %}
jinja extends - dziedziczenie szablonów pozwala na wykożystanie tego samego szablonu do generowania różnych stron
                base.html:
                <html>
                <head>
                    {% block head %}
                        <title>
                            {% block title %}
                            {% endblock %}
                            Jakis tekst
                        </title>
                    {% endblock %}
                </head>
                <body>
                    {% block body_part_1 %}
                    {% endblock %}
                    {% block body_part_2 %}
                    {% endblock %}
                </body>
                </html>

                index.html - w nim najpierw wstawiamy szablon, potem definiujuemy zawartość poszczególnych bloków.
                {% extends "base.html" %}
                {% block title %} Index {% endblock %}
                ...
bootstrap       - definiuje standardowe szablony i CSS. Np blok bazowy: bootstrap/base.html i jego bloki:
                doc Cały dokument HTML.
                html_attribs Atrybuty wewnątrz znacznika <html>.
                html Zawartość znacznika <html>.
                head Zawartość znacznika <head>.
                title Zawartość znacznika <title.>
                metas Lista znaczników <meta>.
                styles Definicje stylów CSS.
                body_attribs Atrybuty wewnątrz znacznika <body>.
                body Zawartość znacznika <body>.
                navbar Pasek nawigacji zdefiniowany przez użytkownika.
                content Treść strony określona przez użytkownika.
                scripts Deklaracje JavaScript znajdujące się na końcu dokumentu
bootstrap super - żeby nie nadpisywać bloków a jedynie je rozszerzać należy w bloku wołać najpierw funkcję super()
                {% block scripts %}
                {{ super() }}
                <script type="text/javascript" src="my-script.js"></script>
                {% endblock %}
url_for         - pozwala na dynamiczne tworzenie łącza.
                url_for("index") - zwraca adres "/"
                url_for("user", name="kaszanka") - zwraca adres "/user/kaszanka"
pliki statyczne - Flask automatycznie dodaje trasę "/static/<filename>" do obsługi plików statycznych (obrazy itp).
                url_for("static", filename="css/styles.css", _external=True) - wygeneruje łącze
                "https://localhost:5000/static/css/styles.css"
flask moment    - pozwala na lokalizowanie dat i czasu. Dobre rowiązanie to używanie UTC an serwerze, a po stronie
                przeglądarki (która ma lokalne ustawienia) wykożystanie standardowego skryptu Moment.js pozwalającego
                na renderowanie czasu UTC do wartości lokalnej.
                Potrzebner są dokładnie 2 skrypty: Moment.js i jQuery.js.
-------------------------------------
Formularze Flask WTF
-------------------------------------
secret key      - tajny klucz, ciąg dowolnych znaków służący za klucz podpisujący lub szyfrujący. Jest to wymagane
                do kożystania z Flask WTF. Sposoby definiowania takiego klucza:
                app = Flask(__name__)
                app.config['SECRET_KEY'] = 'trudny do odgadnięcia ciąg znaków'
                gdzie app.config to słownik przetrzymujący różnego typu zmienne konfiguracyjne Flaska. Klucz powinien
                przechowywany w zmiennej środowiskowej, nie w kodzie.
FlaskForm       - klasa rodzic do każdej innej klasy na serwerze reprezentujacej formularz.
wtforms         - zawiera standardowe pola HTML
                BooleanField Pole wyboru z wartościami True i False.
                DateField Pole tekstowe przyjmujące wartość typu datetime.date w danym formacie.
                DateTimeField Pole tekstowe przyjmujące wartość typu datetime.datetime w danym formacie.
                DecimalField Pole tekstowe przyjmujące wartość typu decimal.Decimal.
                FileField Pole przesyłania pliku.
                HiddenField Ukryte pole tekstowe.
                MultipleFileField Pole przesyłania wielu plików.
                FieldList Lista pól danego typu.
                FloatField Pole tekstowe przyjmujące wartość liczby zmiennoprzecinkowej.
                FormField Formularz osadzony jako pole w formularzu.
                IntegerField Pole tekstowe przyjmujące wartość liczy całkowitej.
                PasswordField Pole tekstowe hasła.
                RadioField Lista przycisków opcji.
                SelectField Rozwijana lista opcji.
                SelectMultipleField Rozwijana lista opcji z wielokrotnym wyborem.
                SubmitField Przycisk przesłania formularza.
                StringField Pole tekstowe.
                TextAreaField Pole tekstu wielowierszowego.
renderowanie    - zamiast ręcznego tworzenia formularza komżystamy z tego co dostarcza bootstrap
                {% import "bootstrap/wtf.html" as wtf %}
validate_on_submit() - zwraca True po poprzewnym zwalidowaniu danych formularza i ich przesłaniu.
user session    - sesja urzytkownika - prywatna pamięć dostępna dla każdego klienta.
                Pozwala zapamietywać dane przychodzące z rządania.
                Domyślnie sesje przechowywane są w plikach cookie po stronie klientów, podpisane kryptograficznie.
                Sesja jest słownikiem w którym możemy definiować nowe klucze i przypisywać im wartości, a następnie
                wykożystywać te dane do wyświetlania na stronie.
flash           - to wsparcie dla wyskakujących okienek - pop ups.
                Wygenerowanie komunikatu: flash("Kounikat do przekazania")
                Renderowanie komunikatu: {% for message in get_flashed_messages() %} {{ message }} {{ endfor }}
-------------------------------------
Bazy danych
-------------------------------------
flask-sqlalchemy - biblioteka integrująca Flask z SQLAlchemy. SQLAlchemy to ORM (Object relational mapper), czyli
                wysokopoziomowy sposób dostępu do bazy danych, z możliwością bezpośredniego dostępu (np w celu
                stworzenia zapytań o lepszej wydajności). Cechy:
                - baza danych podawana jest jako adres URL:
                    MySQL mysql://nazwa_użytkownika:hasło@nazwa_hosta/baza_danych
                    Postgres postgresql://nazwa_użytkownika:hasło@nazwa_hosta/baza_danych
                    SQLite (Linux, macOS) sqlite:////bezwzględna/ścieżka/do/bazy_danych
                    SQLite (Windows) sqlite:///c:/bezwzględna/ścieżka/do/bazy_danych
                    Bazy danych SQLite nie mają serwera, więcj nazwa hosta, użytkownika i hasło są pomijane i
                    zastępowane nazwą pliku z bazą danych.
                - adres URL bazy musi być zapisany jako klucz SQLALCHEMY_DATABASE_URI w obiekcie konfiguracyjnym Flask
                - definiowanie modelu polega na użycie klasy bazowej Model i poprzez jego dziedziczenie tworzeniu
                klas reprezentujących poszczególne tabele w naszej bazie.

"""

import datetime
import os

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, IntegerField, EmailField, FieldList, widgets
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = "moj klucz do szyfrowania"
bootstrap = Bootstrap(app)
moment = Moment(app)

# Konfiguracja bazy danych
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "mojabaza.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role")

    def __repr__(self):
        return f"Role {self.name}"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    priorytet = db.Column(db.Integer())
    email = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return f"User {self.username}"


class MojaForma(FlaskForm):
    name = StringField("Jak masz na imię?", default=None, validators=[DataRequired()])
    priorytet_minimum = 0
    priorytet_maximum = 10
    priorytet = IntegerField(f"Priorytet ({priorytet_minimum} do {priorytet_maximum})", default=0,
                             widget=widgets.NumberInput(min=priorytet_minimum, max=priorytet_maximum))
    email = EmailField("Email")
    submit = SubmitField("Wyslij")


@app.route("/", methods=["GET", "POST"])
def index():
    moja_forma = MojaForma()
    if moja_forma.validate_on_submit():
        name_from_db = User.query.filter_by(username=moja_forma.name.data).first()
        if name_from_db:
            flash(f"Uzytkownik {name_from_db.username} już istnieje.")
        else:
            # Dodanie do bazy danych
            user = User(username=moja_forma.name.data,
                        priorytet=moja_forma.priorytet.data,
                        email=moja_forma.email.data)
            db.session.add(user)
            db.session.commit()
            # Dodanie do cookies
            session["name"] = moja_forma.name.data
            session["priorytet"] = moja_forma.priorytet.data
            session["email"] = moja_forma.email.data
        # tutaj robimy przekierowanie zapobiegające ponownemy wysłaniu formularza w przypadku odświeżenia
        return redirect(url_for("index"))
    return render_template("index.html", current_time=datetime.datetime.utcnow(),
                           moja_forma=moja_forma, name=session.get("name"), priorytet=session.get("priorytet"),
                           email=session.get("email"))


@app.route("/user/<zmienna>")
def user(zmienna):
    lista = [f"{u.username} {u.email} Priorytet {u.priorytet}" for u in User.query.all()]
    return render_template("user.html", name=zmienna, lista=lista, element=2)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Dodawanie kontekstu powłoki
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


if __name__ == "__main__":
    app.run(debug=True)
