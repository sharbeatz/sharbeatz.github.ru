from flask import Flask, render_template, request, redirect,url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__) # основа
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#НОВЫЙ КОММЕНТ

@app.route('/') # главная страница
@app.route('/home') # главная страница
def index():
    return render_template('index.html')


# Характеристики
@app.route('/features')
def features():
    return render_template('features.html')

# Цены
@app.route('/price')
def price():
    return render_template('price.html')

@app.route('/clients')
def clients():
    return render_template('clients.html')



@app.route('/about') # страница о сайте
def about():
    return "About page"


# База данных пользователей
class Users(db.Model):
    __tablename__ = 'users'  # добавляем атрибут __tablename__ с правильным именем таблицы
    id = db.Column(db.Integer, primary_key=True)
    floatingName = db.Column(db.String(50), nullable=False)
    floatingSurname = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    floatingPassword = db.Column(db.String(50), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Users {self.id}>'


# Регистрация
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        floatingName = request.form['floatingName']
        floatingSurname = request.form['floatingSurname']
        login = request.form['login']
        floatingPassword = request.form['floatingPassword']
        confirmPassword = request.form['confirmPassword']  # Получаем подтверждение пароля
        if floatingPassword != confirmPassword:  # Проверяем, совпадают ли пароль и его подтверждение
            return "Пароль и подтверждение пароля не совпадают"
        users = Users(floatingName=floatingName, floatingSurname=floatingSurname, login=login, floatingPassword=floatingPassword)
        try:
            db.session.add(users)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Ошибка: {str(e)}"
    else:
        return render_template("sign_up.html")



# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['floatingPassword']
        user = Users.query.filter_by(login=login).first()

        if user and user.floatingPassword == password:
            session['user_id'] = user.id  # Сохранение идентификатора пользователя в сессии
            flash('Logged in successfully.', 'success')
            logged_in = 'user_id' in session
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

#личный кабинет
@app.route('/dashboard')
def dashboard():
    # Проверка, авторизован ли пользователь
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    # Получение информации о пользователе из базы данных
    user = Users.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))




if __name__ == "__main__": # основа
    app.run(debug=True) # debug = False только при готовом сайте