from os import error
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import config
from datetime import datetime



app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'



# Login information is hosted in the config.py file, which we can use for other information if needed
app.config['MYSQL_HOST'] = config.mysql_host
app.config['MYSQL_USER'] = config.mysql_user
app.config['MYSQL_PASSWORD'] = config.mysql_password
app.config['MYSQL_DB'] = config.mysql_db

# Intialize MySQL
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE userName = %s AND pass = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['userID'] = account['userID']
            session['userName'] = account['userName']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE userID = %s', (session['userID'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['userName'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/Falsk/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE userName = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user (userName, pass, Email) VALUES ( %s, %s, %s)',
                           (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# This is where a new owner will be created
@app.route('/newOwner', methods=['GET', 'POST'])
def newOwner():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'LastName' in request.form and 'FirstName' in request.form and 'Email' in request.form:
        # Create variables for easy access
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        Email = request.form['Email']
        mailingAddress = request.form['mailingAddress']
        mailingAddressLine2 = request.form['mailingAddressLine2']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']

        # Check if owner already exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Owners WHERE Email = %s', (Email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address!'
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     msg = 'Username must contain only characters and numbers!'
        elif not FirstName or not LastName or not Email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new owner into the owner table
            try:
                cursor.execute('INSERT INTO Owners (FirstName, LastName, Email, MailingAddress, MailingAddressLine2, city, state, zip) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)',
                           (FirstName,LastName, Email, mailingAddress, mailingAddressLine2, city, state, zipcode))
                mysql.connection.commit()
                flash('The new Owner was added successfully', 'message')
                return redirect(url_for('home'))
            except:
                flash('Something was incorrectly input within your data, please try again', 'error')
                return render_template('newOwner.html', msg=msg)

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show owner form with message (if any)
    return render_template('newOwner.html', msg=msg)


@app.route('/newLease', methods=['GET', 'POST'])
def newLease():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'startDate' in request.form and 'endDate' in request.form and 'price' in request.form \
         and 'rentalAgent' in request.form and 'tenantID' in request.form and 'propertyID' in request.form:
        # Create variables for easy access
        # Uses strptime to convert date from string in the wrong format to a date in correct format for mySQL
        StartDate = datetime.strptime (request.form['startDate'],'%Y-%m-%d')
        EndDate = datetime.strptime (request.form['endDate'],'%Y-%m-%d')
        Price = request.form['price']
        RentalInsurance = request.form['rentalInsurance']
        rentalAgent = request.form['rentalAgent']
        leaseStatus = 'Active'
        TenantID = request.form['tenantID']
        PropertyID = request.form['propertyID']
        # Check if owner already exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # If account exists show error and validation checks
        
        if not StartDate or not EndDate or not Price or not rentalAgent or not TenantID or not PropertyID:
            msg = 'Please fill out the form!'
        else:
            # Try catch to ensure the validity of the data, will reload the page with error message if not compatable with database
            try:
                cursor.execute(
                    'INSERT INTO Leases (startDate,endDate,price,rentalInsurance,leaseStatus,rentalAgent,tenantID,propertyID) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)',
                    (StartDate,EndDate,Price,RentalInsurance,leaseStatus,rentalAgent,TenantID,PropertyID))
                mysql.connection.commit()
                # This flash is used on the home page and displays a success message when data was sent to the database correctly
                flash('The new lease was added successfully', 'message')
                return redirect(url_for('home'))
            except:
                flash('Something was incorrectly input within your data, please try again', 'error')
                

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show owner form with message (if any)
    return render_template('newLease.html', msg=msg)

@app.route('/newProperty', methods=['GET', 'POST'])
def newProperty():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'propertyID' in request.form and 'propertyAddress' in request.form and 'propertyCity' in request.form and 'propertyState' in request.form and 'propertyZipcode' in request.form and 'numOfBedrooms' in request.form and 'numOfBathrooms' in request.form \
    and 'keyNum' in request.form and 'pets' in request.form and 'bbq' in request.form and 'ac' in request.form and 'washerDryer' in request.form and 'numOfParkingSpots' in request.form and 'outsideShower' \
    in request.form and 'wifiName' in request.form and 'wifiPassword' in request.form and 'beachside' in request.form and 'bayside' in request.form and 'oceanFront' in request.form \
    and 'bayFront' in request.form and 'commissionPercentage' in request.form and ownerID in request.form:
        # Create variables for easy access
        propertyID = request.form['propertyID']
        propertyAddress = request.form['propertyAddress']
        propertyState = request.form['propertyState']
        propertyCity = request.form['propertyCity']
        propertyZipcode = request.form['propertyZipcode']
        numOfBedrooms =request.form['numOfBedrooms']
        numOfBathrooms =request.form['numOfBathrooms']
        keyNum = request.form['keyNum']
        pets = request.form['pets']
        bbq = request.form['bqq']
        ac = request.form['ac']
        washerDryer = request.form['washerDryer']
        numOfParkingSpots = request.form['numOfParkingSpots']
        outsideShower = request.form['outsideShower']
        wifiName = request.form['wifiName']
        wifiPassword = request.form['wifiPassword']
        beachside = request.form['beachside']
        bayside = request.form['bayside']
        oceanFront = request.form['oceanFront']
        bayFront = request.form['bayFront']
        commissionPercentage = request.form['commissionPercentage']
        ownerID = request.form['ownerID']


        # Check if owner already exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Properties WHERE propertyAddress = %s', (propertyAddress,))
        property = cursor.fetchone()
        # If account exists show error and validation checks
        if property:
            msg = 'Property already exists!'
        elif not propertyID or not propertyAddress or not propertyState or not propertyCity or not propertyZipcode or not numOfBedrooms \
                or not numOfBathrooms or not keyNum or not pets or not bbq or not ac or not washerDryer or not numOfParkingSpots or not outsideShower or not wifiName \
                or not wifiName or not wifiPassword or not beachside or not bayside or not oceanFront or not bayFront or not commissionPercentage or not ownerID:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new owner into the owner table
            cursor.execute(
                'INSERT INTO Leases (propertyID,propertyAddress,propertyCity,propertyState,propertyZipcode,numOfBedrooms,numOfBathrooms,keyNum,pets,ac,bbq,washerDryer,numOfParkingSpots,outsideShower,wifiName,wifiPassword,beachside,bayside,oceanFront,bayFront,commissionPercentage,ownerID) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (propertyID,propertyAddress,propertyCity,propertyState,propertyZipcode,numOfBedrooms,numOfBathrooms,keyNum,pets,ac,bbq,washerDryer,numOfParkingSpots,outsideShower,wifiName,wifiPassword,beachside,bayside,oceanFront,bayFront,commissionPercentage,ownerID))
            mysql.connection.commit()
            # TODO set up a message for users that successfully created an owner on the home page as a popup or something
            return redirect(url_for('home'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show owner form with message (if any)
    return render_template('newProperty.html', msg=msg)

@app.route('/newTenant', methods=['GET', 'POST'])
def newTenant():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'tenantID' in request.form and 'LastName' in request.form and 'FirstName' in request.form and 'tenantMailingAddress' in request.form\
    and 'tenantPhone' in request.form and 'tenantEmail' in request.formand and 'tenantCity' in request.form and 'tenantState' in request.form and 'tenantZip' in request.form:
    # Create variables for easy access
        tenantID = request.form['tenantID']
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        tenantMailingAddress = request.form['tenantMailingAddress']
        tenantPhone = request.form['tenantPhone']
        tenantEmail = request.form['tenantEmail']
        tenantCity = request.form['tenantCity']
        tenantState = request.form['tenantState']
        tenantZipcode = request.form['tenantZipcode']


        # Check if owner already exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Leases WHERE LeaseID = %s', (tenantID,))
        tenant = cursor.fetchone()
        # If account exists show error and validation checks
        if tenant:
            msg = 'Tenant already exists!'
        elif not tenantID or not LastName or not FirstName or not tenantMailingAddress or not tenantPhone or not tenantEmail\
        or not tenantCity or not tenantState or not tenantZipcode :
            msg = 'Please fill out the form!'
        else:
    # Account doesnt exists and the form data is valid, now insert new owner into the owner table
            cursor.execute(
            'INSERT INTO Tenant (tenantID,LastName,FirstName,tenantMailingAddress,tenantPhone,tenantEmail,tenantCity,tenantState,tenantZipcode) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (tenantID, LastName, FirstName, tenantMailingAddress, tenantPhone, tenantEmail, tenantCity, tenantState, tenantZipcode))
        mysql.connection.commit()
    # TODO set up a message for users that successfully created a new Tenant on the home page as a popup or something
        return redirect(url_for('home'))

    elif request.method == 'POST':
    # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show owner form with message (if any)
    return render_template('newTenant.html', msg=msg)



if __name__ == '__main__':
    app.run()
