from flask import Flask, render_template, g, request
from werkzeug.utils import redirect
from flask_login import login_user, LoginManager, AnonymousUserMixin, current_user, login_required, logout_user
from configuration import Config
from data import db_session
from data.user import User
from data.draft import Draft
from forms.login import LoginForm
from forms.register import RegisterForm


app = Flask(__name__)
app.config.from_object(Config)


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = '0'


login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.init_app(app)


@app.before_request
def before_request():
    g.user = current_user


@app.route("/", methods=['GET'])
def index():
    return redirect('/login')



@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """Предполагается, что на страницу регистрации пользователь попадает либо по ссылке,
    Либо его регистрирует в системе другой человек, у которого будет доступ."""

    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if (session.query(User).filter(User.phone == form.phone.data).first()):
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            phone=form.phone.data
            #position=form.position.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.phone == form.phone.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f'/user/{g.user.id}')
        if not user:
            return render_template('login.html',
                                   message="Такого пользователя не существует",
                                   form=form)
        return render_template('login.html',
                               message="Неверный телефон или пароль",
                               form=form)
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(User, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/user/<int:id>', methods=['GET', 'POST'])
def user_profile(id):
    session = db_session.create_session()
    user = session.query(User).filter_by(id=id).first()
    if user == None:
        return render_template('404.html', id=id), 404
    if current_user.id != id:
        return render_template('403.html'), 403
    return redirect("/")

def main():
    db_session.global_init("db/users.sqlite")
    app.run()


if __name__ == '__main__':
    app.debug = True
    main()