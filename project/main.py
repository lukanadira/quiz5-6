from flask import Flask, redirect, url_for, render_template, request, session, flash
import requests
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Luka_da_Vakho'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite'
db = SQLAlchemy(app)

class Users(db.Model):
    username = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f' Username: {self.username}; Password: {self.password}'

db.create_all()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['psw']
        session['username'] = username
        session['psw'] = password
        if username == '' or password == '':
            flash('შეიყვანეთ ყვველა მონაცემი', 'error')

        else:
            User = Users(username=username, password=int(password))
            db.session.add(User)
            db.session.commit()
            flash('თქვენი მონაცემები შენახულია მონაცემთა ბაზაში')
            return redirect(url_for('login'))
    return render_template('registration.html')


@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['weathername']
        session['weathername'] = city
        api_key = '1d849b5d5e5e96d7c173de74ee2f6028'
        resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        resour = json.loads(resp.text)
        resp_json_structured = json.dumps(resour, indent=4)
        with open("amindi.json", "w") as file:
            json.dump(resour, file, indent=4)
        k = resour['main']
        temp = round(k['temp'], 0)
        return f'temperature in {city} is {temp} &#8451'

    return render_template('weather.html')



@app.route('/polution', methods=['GET', 'POST'])
def polution():
    if request.method == 'POST':
        lat = request.form['latitude']
        lon = request.form['longitude']
        session['latitude'] = lat
        session['longitude'] = lon
        url = "https://weatherbit-v1-mashape.p.rapidapi.com/alerts"

        querystring = {"lat": str(lat), "lon": str(lon)}

        headers = {
            'x-rapidapi-key': "32e88e87b2mshe448507df4d40b7p113158jsn78622339dd1e",
            'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response
    return render_template('polution.html')


@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'you are logged out'

@app.route('/admins', methods=['GET', 'POST'])
def admins():
    if request.method == 'POST':
        admin_pass = request.form['pas']
        session['pass'] = admin_pass
        if admin_pass != 'luka':
            flash('პაროლი არასწორია', 'error')
        else:
            return render_template('profile.html')
    return render_template('admins.html')




if __name__ == "__main__":
    app.run(debug=True)