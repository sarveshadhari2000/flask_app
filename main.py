from __init__ import *
from models import User,Client
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from admin import AdminView,ClientView, ExcelView
from flask_admin.contrib.fileadmin import FileAdmin


admin = Admin(app, name='Dashboard', index_view=AdminView(User, db.session, url='/pythonlogin/admin'),template_mode="bootstrap2")
admin.add_view(ClientView(Client,db.session))
admin.add_view(ExcelView(name='Excel', endpoint='excel'))





# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        account = User.query.filter_by(name=username).first()
       
                # If account exists in accounts table in out database
        if account and check_password_hash(account.password, password):
            # Create session data, we can access this data in other routes

            print(account)
            
            session['loggedin'] = True
            session['id'] = account.userId
            session['username'] = account.name
            session['email'] = account.email
            login_user(account)
            # Redirect to home page
            return redirect( request.args.get('next') or url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html',title="Login")



# http://localhost:5000/pythinlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        account = User.query.filter_by(name=username).first()
        # If account exists show error and validation checks
        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            new_user = User(email=email, name=username, password=generate_password_hash(password, method='sha256')) #
        # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!", "danger")
    # Show registration form with message (if any)
    return render_template('auth/register.html',title="Register")

# http://localhost:5000/pythinlogin/home 
# This will be the home page, only accessible for loggedin users

@app.route('/pythonlogin/home')
@login_required
def home():
    # Check if user is loggedin
   
        # User is loggedin show them the home page
    return render_template('home/home.html', username=session['username'],title="Home")
    # User is not loggedin redirect to login page

@app.route('/pythonlogin/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('login'))   


@app.route('/pythonlogin/profile')
@login_required
def profile():
    # Check if user is loggedin
        # User is loggedin show them the home page
    return render_template('auth/profile.html', user=current_user,title="Profile")
    # User is not loggedin redirect to login page

@login_required
@app.route('/pythonlogin/calculate_profits',methods=['GET', 'POST'])
def calculate_profits():
    
    if request.method == "POST":

        f = request.files['excel']

        return "HERH"
    

if __name__ =='__main__':
	app.run(debug=True)
