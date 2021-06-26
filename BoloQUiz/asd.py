from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.sqlite'
app.config['SQLALCHEMY_BINDS']= {'two' : 'sqlite:///user.sqlite'}
db = SQLAlchemy(app)

class User(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    dev = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)


    def __str__(self):
        return f'Game - {self.name},\nRating - {self.rating},\nDeveloper - {self.dev}.'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username != '' and password != '':
            user_find = User.query.filter_by(username=username, password=password).all()
            if len(user_find) > 0:
                session['username'] = username
                return render_template('addgame.html')
            else:
                flash("NO user found", 'error')
        else:
            flash("Fill all inputs", 'error')

    # return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/game')
def game():
    all_game = Games.query.all()
    return render_template('game.html', all_game=all_game)

@app.route('/addgame', methods=['GET', 'POST'])
def addgame():
    if request.method=='POST':
        n = request.form['name']
        d = request.form['dev']
        r = request.form['rating']
        if n == '' or d == '' or r == '':
            flash('Fill all forms', 'error')
        elif not r.isnumeric():
            flash('Rating must be NUMBER', 'error')
        else:
            g1 = Games(name=n, dev=d, rating=int(r))
            db.session.add(g1)
            db.session.commit()
            flash('Game was added to the list', 'info')

    return render_template('addgame.html')


@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        if repassword == password and password != '' and username != '':
            username_find = User.query.filter_by(username=username).all()
            if len(username_find) == 0:
                u1 = User(username=username, password=password)
                db.session.add(u1)
                db.session.commit()
                flash("User was successfully added!", 'info')
            else:
                flash("User already exists!", 'error')
        else:
            flash("Passwords do not match or fields are empty!", 'error')
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)


# Team members:
#  Nika Jvelauri
#  Luka Sharikadze
