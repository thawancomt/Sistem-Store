
Here's an improved version of your README:

# ERP System with Python

An ERP system built with Flask, Python, JavaScript, TailwindCSS, MySQL, SQLAlchemy, and more.

## Features

- **Login and User Registration:** Secure user authentication and registration system.
- **Access Levels:** Different levels of access for users.
- **Admin Control:** Admins have high-level control over the system.
- **Production Management:** Release and control production, with dynamic chart visualizations.
- **Stock Management:** Manage and visualize stock releases through charts.
- **Article Management:** Create and set parameters for articles.
- **Store Management:** Create and manage different stores.
- **User Store Association:** Associate users with specific stores to control access.
- **Chart Types:** Three different chart types: bar, line, and pie.
- **Article Unit Management:** Create units, aliases, and descriptions for articles.

These features demonstrate practical application of knowledge in real-world scenarios.

## Screenshots

### Login Methods
![Login](https://github.com/thawancomt/Sistem-Store/assets/131563700/a2340d9e-cda0-4711-857c-b6eb3a8efa49)
![Login](https://github.com/thawancomt/Sistem-Store/assets/131563700/9f5924f2-6ef3-494c-b46b-6c7a9b3d4da2)

### User Registration
![Register Users](https://github.com/thawancomt/Sistem-Store/assets/131563700/cf58b0a8-6c34-4dd1-8c85-65c20c945c95)
![Register Users](https://github.com/thawancomt/Sistem-Store/assets/131563700/2c074932-6624-4481-943f-9434d6a8d56d)
# Charts

### Production chart
![image](https://github.com/thawancomt/Sistem-Store/assets/131563700/034d32b8-7ad5-48b8-9c17-febe0dd676f3)
![image](https://github.com/thawancomt/Sistem-Store/assets/131563700/435e5844-c5ef-4e06-b318-9c69b7ca45ee)

## Chart filtered
![image](https://github.com/thawancomt/Sistem-Store/assets/131563700/767298de-0e73-4f28-a6ca-4a72edeb36f3)
## Project Structure

```plaintext
flaskr (root)
├── blueprints
│   └── ...
├── app.py
├── run.py
└── CONFIG.py
```

### Project Design

The project follows a modular structure where each route has its own blueprint with its own static and template folders. This makes it easy to understand and maintain each route individually. The project also uses a base HTML template to reduce boilerplate code, ensuring that common elements like navigation, headers, and CSS links are written only once.

### Why Flask?

`Flask` was chosen for its simplicity and ease of use. It allows easy expansion and control over the project. Flask's plugins, such as `flask-SQLAlchemy`, facilitate seamless integration with SQLAlchemy ORM. 

`MySQL` was chosen for its robustness, adding complexity but offering infinite possibilities.

### Example Code
#### In this section we will see some examples of code to understand more about the why did I chosen Flask and its plugins.

#### `ProductionService.py`

#### `Querying` and `Insert` the Database is simple.

```python
from datetime import datetime, timedelta

def get_production_history(self):
    today = self.date
    tomorrow = (datetime.strptime(today, '%Y-%m-%d') + timedelta(days=1))
    
    return (
        db.session.query(Production)
        .filter(
            and_(
                Production.store_id == self.store_id,
                Production.date >= today,
                Production.date <= tomorrow,
            )
        )
        .all()
    )

def insert_production(self, data):
    date = data.get('date')
    if date:
        del data['date']
        
    for article_id, quantity in data.items():
        if int(quantity) > 0:
            new_production = Production(
                store_id=self.store_id,
                creator_id=self.creator_id,
                article_id=article_id,
                quantity=quantity,
                date=date
            )
            db.session.add(new_production)
            
    db.session.commit()
```

#### Using `flask-login`

Initially, a custom login and session management system was created, but it became complex to maintain. Instead of it `flask-login` was implemented for easier session and login management.

#### `LoginView.py`

```python
@authentication.route('/', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if LoginService(email=email, password=password).login():
        return redirect(url_for('homepage.home'))
    
    flash('Invalid email or password', 'danger')
    return redirect(url_for('auth.login_page'))
```

#### `LoginService.py`

```python
class LoginService:
    def __init__(self, email=None, password=None):
        if email is None or password is None:
            return self.logout()
        
        self.email = email
        self.password = password
        self.user = UserService(email=self.email).get_user_by_email()

    def login(self) -> bool:
        if self.user and self.verify_password(self.user.password):
            self.user.last_login = datetime.now()
            db.session.commit()
            login_user(self.user)
            return True
        
        return False
```
### The Admin and the managers that has access to the system can created task to do
![image](https://github.com/thawancomt/Sistem-Store/assets/131563700/5897e1fc-a43d-4c4b-a3fc-391c33e4d581)

### Also we have the Daily Task
You can set up tasks for gonna be show as daily tasks to be done, imagine has a task that you need to do every day, so you can create a daily task to manage it, and it has a complexity logic behind it, so if you put this created task as completed it wont disappear, but will stop to be showed in the nexts days.


## Installation

```bash
pip install -r requirements.txt
python -u System/app.py
```

- [@thawancomt](https://www.github.com/thawancomt)

## Skills

Python, Flask, MySQL, SQLAlchemy, HTML, CSS, Flask-Login, Flask-SQLAlchemy

---

This README provides a comprehensive overview of your ERP system, detailing its features, structure, and design choices while including code examples and installation instructions.
