from flask import Flask, redirect, render_template, request, flash
from managers.users import User, Login, CreateUser

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def about():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        connected_user = User()
        connected_user.email = email
        connected_user.password = password

        result = Login(connected_user).validate()

        if result:
            return redirect('/homepage')

    return render_template('login.html')


@app.route('/homepage')
def home():
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
