import os
from datetime import datetime
from flask import Flask, render_template, g, request, flash
from werkzeug.utils import redirect, secure_filename
from flask_login import login_user, LoginManager, AnonymousUserMixin, current_user, login_required, logout_user
from configuration import Config
from data import db_session
from data.user import User
from data.draft import Draft
from format_handler import rename_file_on_server, SLT_to_PDF, DWG_to_PDF
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.user_drafts import DraftForm

app = Flask(__name__)
app.config.from_object(Config)


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = '0'


login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.init_app(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.before_request
def before_request():
    g.user = current_user


@app.route("/", methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect('/news')
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
        if (session.query(User).filter(User.phone == form.phone.data).first()) or (
                session.query(User).filter(User.email == form.email.data).first()):
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            phone=form.phone.data,
            position=form.position.data,
            email = form.email.data        )
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
    else:
        fio = user.name
        phone = user.phone
        email = user.email
        position = user.position
        my = g.user.id
    return render_template('user_profile.html', fio=fio, position=position, email=email, phone=phone,
                           my=my)



@app.route('/user/<int:id>/drafts', methods=['GET', 'POST'])
def users_drafts(id):
    """Загрузка чертежей, обработка загрузки файлов, перевод в pdf"""
    session = db_session.create_session()
    user = session.query(User).filter_by(id=id).first()
    form = DraftForm()
    if user == None:
        flash('User ' + id + ' not found.')
        return render_template('login.html')
    else:
        my = g.user.id
        user_cur = session.query(User).filter_by(id=my).first()
        user_id = int(id)
        file = form.file_url.data

        if not os.path.exists(app.config['UPLOAD_FOLDER_USER'] + f'{user_id}'):
            os.makedirs(app.config['UPLOAD_FOLDER_USER'] + f'{user_id}')
        if not os.path.exists(app.config['UPLOAD_FOLDER_USER'] + f'{user_id}/drafts'):
            os.makedirs(app.config['UPLOAD_FOLDER_USER'] + f'{user_id}/drafts')

        if file and allowed_file(file.filename):
            file.filename = rename_file_on_server(secure_filename(file.content_type)[6:],
                                         app.config['UPLOAD_FOLDER_USER'] + f'{user_id}')
            filename = secure_filename(file.filename)
            way_to_file = os.path.join(app.config['UPLOAD_FOLDER_USER'] + f'{user_id}/', filename)

            way_to_save = None
            if secure_filename(file.content_type).lower() == 'stl':
                way_to_save = SLT_to_PDF(filename, way_to_file)
            if secure_filename(file.content_type).lower() == 'dwg':
                way_to_save = DWG_to_PDF(filename, way_to_file)
            if way_to_file != None:
                draft = Draft(
                    user_id=user_id,
                    name=filename,
                    upload_date=datetime.now().strftime("%A %d %b %Y"),
                    way_to_file=way_to_save,
                    original_extension=secure_filename(file.content_type).lower(),)
                session.add(draft)
                session.commit()
                flash("Файл загружен.")
                return redirect(f'{id}')
            else:
                os.remove(way_to_file)
                flash("Невозможно загрузить данный файл")
        else:
            flash("Файл не выбран")
        users_drafts = session.query(Draft).filter_by(autor_id=user_id).order_by(Draft.id.desc())
        return render_template('drafts.html', user_id=user_id, my_id=my,
                              form=form, drafts=users_drafts,id=id, user=user, me=user_cur)



app.route('/user/<user:id/tasks>')
def tasks(id):
    session = db_session.create_session()
    user = session.query(User).filter_by(id=id).first()
    if user == None:
        return render_template('404.html', id=id), 404
    if current_user.id != id:
        return render_template('403.html'), 403
    else:
        # Переделать форму и таблицу в бд, пока плохо продуманно
        return render_template('tasks.html', id=user)


app.route('/user/<int:id/tasks/<int:task_id>')
def one_task(id, tasks_id):
    """Страница одной задачи"""
    pass



@app.route('/user/<int:id>/<int:id_chat>')
def chat(id, id_chat):
    """Чат с другими сотрудниками/сотрудником"""
    pass


# Курсы и новости должны быть без обработки - чистая верстка для демонстрации

@app.route('/curses')
def courses():
    return render_template('curses.html')


@app.route('/news')
def main_news():
    """Вывод новостей на вкладке новости и при входе в акк
    Возможо загрузка из БД с новостями, под вопросом"""
    return render_template('news.html')



def main():
    db_session.global_init("db/users.sqlite")
    app.run()


if __name__ == '__main__':
    app.debug = True
    main()