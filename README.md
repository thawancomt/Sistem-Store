# ERP system with python
An ERP system that uses Flask, Python, JavaScrit, TailwindCSS, MySQL, SQLALCHEMY and much more.

# Features - what this system allow you to do?
- `login`
- `register users`
- `Users has differents level of access`
- `Admin has high level control`
- `production control`
- `stock control`
- `articles creation`
- `You can create differents stores to manage `
- `Each user can be associated with an store`
- `Stock with chart visualization`
- `charts has 3 differents types (bar, line, pie)`

All these features just show that I know apply my knowledge in real world situation.

## login Methods:
![image](https://github.com/thawancomt/Sistem-Store/assets/131563700/a2340d9e-cda0-4711-857c-b6eb3a8efa49)
![image](https://github.com/thawancomt/Sistem-Store/assets/131563700/9f5924f2-6ef3-494c-b46b-6c7a9b3d4da2)

## Register users:
![image](https://github.com/thawancomt/Sistem-Store/assets/131563700/cf58b0a8-6c34-4dd1-8c85-65c20c945c95)
![image](https://github.com/thawancomt/Sistem-Store/assets/131563700/2c074932-6624-4481-943f-9434d6a8d56d)

# Structure 
``` python
The project Structure is:
    - flaksr (root)
        | blueprints
             ....
        - app.py
    run.py
    CONFIG.py

```
# Explaining my decision for this project
Basically this project work with modularization, each route have it own blueprint with it own static and template folder, it allows us to understand more easily what each route does and the process to maintain it is so simple.
```
## example:
- Each route has it own blueprint
    - and each blueprint has it own static and template folder
    ...
| the project have an base html to reduce boilerplate, so it was needed
  to be write just 1 time, like nav, header, css links...etc
```

### Why Flask?

`Flask` was choosed cause it is light and simple to use and understand, it allow us to expand easily and control what we want and what we not.
Flask also has a lot of plugins that is easy to apply and integrate in the project, an example is the `flask-SqlALchemy` plugin, this flask plugin allow us to interact easily with `SQLALCHEMY` ORM, by the way:
`MySQL` was choosed because its strong, it put some complexity to the project but allow us infinite possibilities.
```python
# Where db is an sqlalchemy model object

def get_production_history(self):

        # the date is get through the url if it are gaven if not by the datetime
        today = self.date

        tomorrow = (datetime.strptime(today, '%Y-%m-%d') + timedelta(days=1))
        
        # An example of a simple query to get the historic of production 
        return (
            db.session.query(Production) # SELECT
            .filter( # WHERE
                and_( # Condition 
                    Production.store_id == self.store_id,
                    Production.date >= today,
                    Production.date <= tomorrow,
                )
            )
            .all() # Return all results
        )

        # If not have any production it will return an empty list.
```

I also have implemented `sqllite3` but `sqllite3` has some limitations when we want to do relationships between the databases and some queries.

To manage the session, in the beginning I have created my own system to manage the login and keep session, but it was complex to maintain as the project have getting bigger, so this is the why I have implemented `flask-login` plugin.
`flask-login` help us to handle the session and login in our website easily.
example:

LoginView.py
```python
    @authentication.route('/', methods=['POST'])
    def login():
        email = request.form.get('email')
        password = request.form.get('password')
        
        # With one line we made the login
        if LoginService(email = email, password = password).login():
            return redirect(url_for('homepage.home'))
        
        flash('Invalid email or password', 'danger')
        return redirect(url_for('auth.login_page'))
```

LoginService.py
```python
# when we pass the parameters to the LoginService it, automatically get the user

def __init__(self, email = None, password = None) -> None:
        
        if email is None or password is None:
            return self.logout()
        
        self.email = email
        self.password = password
        self.user = UserService(email=self.email).get_user_by_email()

# So now all we need to do is call the login method in the LoginService object
def login(self) -> bool:
        if self.user and self.verify_password(self.user.password):
            self.user.last_login = datetime.now()
            db.session.commit()            
            login_user(self.user)
            return True
        
        return False

```

- [@thawancomt](https://www.github.com/thawancomt)
## 🛠 Habilidades
Python, Flask, MySQL,SqlALchemy, HTML, CSS, Flask-LOGIN, Flask-SQLALCHEMY...

## Instalação

```bash
    pip install -r requirements.txt
    python -u System/app.py
