

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

from forms import LoginForm
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_base_users.db'
csrf = CSRFProtect(app)
db.init_app(app)


@app.route('/')
@app.route('/index/')
def index():
    return render_template('base.html')


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    print(form)
    print(app.config['SECRET_KEY'])

    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        password_hash = generate_password_hash(password)
        user = User.query.filter_by(email=email).first()

        if user:
            form.email.data = 'Пользователь уже существует!'
            return render_template('register.html', form=form)

        else:
            user = User(firstname=firstname, lastname=lastname, email=email, password=password_hash)
            db.session.add(user)
            db.session.commit()
            return 'Пользователь зарегистрирован!'

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()

