# Imports
from os import error
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import config
import json
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

session
# This allows for a user to be logged in
@app.route('/', methods=['GET', 'POST'])
def login():
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
    # Show the login form 
    return render_template('index.html')


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

# http://localhost:5000/Flask/register - this will be the registration page, we need to use both GET and POST requests
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


######################################################## OWNER SECTION ######################################################

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
        # noinspection PyInterpreter
        if account:
            flash('An owner with this email address already exists.', 'error')
            return render_template('newOwner.html', msg=msg)
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

# This is the page where a user can choose how to search for the owner they're looking for
@app.route('/searchOwner/', methods=['GET', 'POST'])
def searchOwnerPage():
    return render_template('searchOwner.html')


# This method is used to search for an owner by their ID
@app.route('/searchOwnerByID/', methods=['GET', 'POST'])
def searchOwnerByID():
    if request.method == 'POST':
        # Create variables for easy access
        ownerID = request.form['ownerID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Owners WHERE ownerID = %s', (ownerID,))
        # Fetch one record and return result
        owner = cursor.fetchone()
        ownerArray =[owner]
        # If account exists in accounts table in out database
        if owner:
            print(owner)
            print("Hello")
            print(ownerArray)
            return render_template('ownerResults.html', owner=ownerArray)
        else:
            # Account doesnt exist or username/password incorrect
             flash('Nah fam', 'message')
    return render_template('searchOwner.html')

# This method is used to search for an owner by their name
@app.route('/searchOwnerByName/', methods=['GET', 'POST'])
def searchOwnerByName():
    if request.method == 'POST':
        # Create variables for easy access
        LastName = request.form['LastName']
        LastName = '%' + LastName + '%'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Owners WHERE LastName LIKE %s', (LastName,))
        # Fetch one record and return result
        owner = cursor.fetchall()
        
        # If account exists in accounts table in out database
        if owner:
            return render_template('ownerResults.html', owner=owner)
        else:
            # Account doesnt exist or username/password incorrect
             flash('There is no user that matches that information, please try again', 'message')
    return render_template('searchOwner.html')



########################################################## TENANT SECTION ######################################################

# This is where a new tenant will be created
@app.route('/newTenant', methods=['GET', 'POST'])
def newTenant():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'LastName' in request.form and 'FirstName' in request.form and 'tenantMailingAddress' in request.form\
    and 'tenantPhone' in request.form and 'tenantEmail' in request.form and 'tenantCity' in request.form and 'tenantState' in request.form and 'tenantZipcode' in request.form:
    # Create variables for easy access
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        tenantMailingAddress = request.form['tenantMailingAddress']
        tenantMailingAddressLine2 = request.form['tenantMailingAddressLine2']
        tenantPhone = request.form['tenantPhone']
        tenantEmail = request.form['tenantEmail']
        tenantCity = request.form['tenantCity']
        tenantState = request.form['tenantState']
        tenantZipcode = request.form['tenantZipcode']

        # Check if owner already exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Tenant WHERE Email = %s', (tenantEmail,))
        tenant = cursor.fetchone()
        # If account exists show error and validation checks
        if tenant:
            print("Already Exists")
            flash('A tenant with this email address already exists.', 'error')
        elif not LastName or not FirstName or not tenantMailingAddress or not tenantPhone or not tenantEmail\
        or not tenantCity or not tenantState or not tenantZipcode :
            print("not entered properly")
            flash('Property not created, please ensure the entire form was filled out.', 'error')
        else:
    # Account doesnt exists and the form data is valid, now insert new owner into the owner table
            try:
                cursor.execute(
                'INSERT INTO Tenant (LastName,FirstName, mailingAddress, mailingAddressLine2, phoneNumber,Email,mailingCity,mailingState,mailingZip) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (LastName, FirstName, tenantMailingAddress,tenantMailingAddressLine2, tenantPhone, tenantEmail, tenantCity, tenantState, tenantZipcode))
                mysql.connection.commit()
                flash('The new tenant was added successfully', 'message')
                return redirect(url_for('home'))
            except:
                print("Failed insert")
                flash('Something was incorrectly input within your data, please try again', 'error')
                
    elif request.method == 'POST':
    # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show owner form with message (if any)
    return render_template('newTenant.html', msg=msg)


# This is the page where a user can choose how to search for the tenant they're looking for
@app.route('/searchTenant/', methods=['GET', 'POST'])
def searchTenantPage():
    return render_template('searchTenant.html')

# This method is used to search for a tenant by their ID
@app.route('/searchTenantByID/', methods=['GET', 'POST'])
def searchTenantByID():
    if request.method == 'POST':
        # Create variables for easy access
        tenantID = request.form['tenantID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Tenant WHERE tenantID = %s', (tenantID,))
        # Fetch one record and return result
        tenant = cursor.fetchone()
        # If account exists in accounts table in out database
        if tenant:
            return render_template('tenantResults.html', tenant=tenant)
        else:
             print("dont Exist")
            # Account doesnt exist or username/password incorrect
             flash('Nah fam', 'message')
    return render_template('searchTenant.html')

# This method is used to search for a tenant by their name
@app.route('/searchTenantByName/', methods=['GET', 'POST'])
def searchTenantByName():
    if request.method == 'POST':
        # Create variables for easy access
        LastName = request.form['TenantLastName']
        LastName = '%' + LastName + '%'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Tenant WHERE LastName LIKE %s', (LastName,))
        # Fetch one record and return result
        tenant = cursor.fetchone()
        # If account exists in accounts table in out database
        if tenant:
            return render_template('tenantResults.html', tenant=tenant)
        else:
            # Account doesnt exist or username/password incorrect
             flash('There is no user that matches that information, please try again ', 'message')
    return render_template('searchTenant.html')



########################################################## PROPERTY SECTION ######################################################

# This is where a new property will be created
@app.route('/newProperty', methods=['GET', 'POST'])
def newProperty():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'propertyAddress' in request.form and 'propertyCity' in request.form \
            and 'propertyState' in request.form and 'propertyZipcode' in request.form \
            and 'numOfBedrooms' in request.form and 'keyNum' in request.form and 'ownerID' in request.form:
        # Create variables for easy access
        print('Before Variables')
        propertyAddress = request.form['propertyAddress']
        propertyAddressLine2 = request.form['propertyAddressLine2']
        propertyState = request.form['propertyState']
        propertyCity = request.form['propertyCity']
        propertyZipcode = request.form['propertyZipcode']
        numOfBedrooms = request.form['numOfBedrooms']
        numOfBathroom = request.form['numOfBathrooms']
        keyNum = request.form['keyNum']
        pets = request.form['pets']
        pool = request.form['pool']
        bbq = request.form['bbq']
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
        print('Before Cursor')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print('Before Property')
        cursor.execute('SELECT * FROM Property WHERE propertyAddress = %s', (propertyAddress,))
        property = cursor.fetchone()
        # If account exists show error and validation checks
        if property:
            print("Already Exists")
            flash('A property with this address already exists.', 'error')
        elif not propertyAddress or not propertyState or not propertyCity or not propertyZipcode or not numOfBedrooms \
                or not numOfBathroom or not keyNum or not numOfParkingSpots or not wifiName \
                or not wifiPassword or not commissionPercentage or not ownerID:
            print("not entered properly")
            flash('Property not created, please ensure the entire form was filled out.', 'error')
        else:
            try:
                print('Hello World')
                # Account doesnt exists and the form data is valid, now insert new owner into the owner table
                cursor.execute(
                    'INSERT INTO Property (propertyAddress,propertyAddressLine2,propertyCity,propertyState,propertyZip,numOfBedroom,numOfBathroom,keyNumber,pets,pool,airConditioning,bbq,washerDryer,numOfParkingSpots,outsideShower,wifiName,wifiPassword,beachside,bayside,oceanFront,bayFront,commissionPercentage,OwnerID) VALUES '
                    '( %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (propertyAddress,propertyAddressLine2, propertyCity, propertyState, propertyZipcode, numOfBedrooms,
                     numOfBathroom, keyNum, pets, pool, ac, bbq, washerDryer, numOfParkingSpots, outsideShower, wifiName,
                     wifiPassword, beachside, bayside, oceanFront, bayFront, commissionPercentage, ownerID))
                mysql.connection.commit()
                flash('The new lease was added successfully', 'message')
                return redirect(url_for('home'))
            except:
                print("Failed insert")
                flash('Something was incorrectly input within your data, please try again', 'error')

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        print('original if statemnt failing')
        msg = 'Please fill out the form!'
    # Show owner form with message (if any)
    return render_template('newProperty.html', msg=msg)


#This is the page where a user can determine how to search for the property they are looking for
@app.route('/searchProperty/', methods=['GET', 'POST'])
def searchPropertyPage():
    return render_template('searchProperty.html')

#TODO add more ownerID as a search option

# This method is used to search for a property by its ID
@app.route('/searchPropertyByID/', methods=['GET', 'POST'])
def searchPropertyByID():
    if request.method == 'POST':
        # Create variables for easy access
        propertyID = request.form['propertyID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Property WHERE propertyID = %s', (propertyID,))
        # Fetch one record and return result
        property = cursor.fetchone()
        # If account exists in accounts table in out database
        if property:
            return render_template('propertyResults.html', property=property)
        else:
             print("dont Exist")
            # Account doesnt exist or username/password incorrect
             flash('Nah fam', 'message')
    return render_template('searchProperty.html')

# This method is used to search for a property by its address
@app.route('/searchPropertyByAddress/', methods=['GET', 'POST'])
def searchPropertyByAddress():
    if request.method == 'POST':
        # Create variables for easy access
        propertyAddress = request.form['propertyAddress']
        propertyAddress = '%' + propertyAddress + '%'

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Property WHERE propertyAddress LIKE %s', (propertyAddress,))

        # Fetch one record and return result
        property = cursor.fetchone()

        # If account exists in accounts table in out database
        if property:
            return render_template('propertyResults.html', property=property)
        else:
             print("dont Exist")
            # Account doesnt exist or username/password incorrect
             flash('Nah fam', 'message')
    return render_template('searchProperty.html')



# This method is used to search for a property by its attributes other than Address or ID
@app.route('/searchPropertyByAttributes/', methods=['GET', 'POST'])
def searchPropertyByAttributes():
    if request.method == 'POST':
        # Create variables for easy access, if the user didn't fill out a field, set variable to "IS NOT NULL"
        
        
        bbq = request.form['bbq']
        if int(bbq) == 0:
            bbq = ' IS NOT NULL '
        else:
            bbq = '= ' + bbq + ' '
        
        pool = request.form['pool']
        if int(pool) == 0:
            pool = ' IS NOT NULL '
        else:
            pool = '= ' + pool + ' '
        
        pets = request.form['pets']
        if int(pets) == 0:
            pets = ' IS NOT NULL '
        else:
            pets = '= ' + pets + ' '
        
        beachside = ""
        bayside = ""
        beachsideBayside = request.form['beachsideBayside']

        if int(beachsideBayside) == 0:
            beachside = ' IS NOT NULL '
            bayside = ' IS NOT NULL '
        elif int(beachsideBayside) == 1:
            beachside = '= 1 '
            bayside = ' IS NOT NULL '
        elif int(beachsideBayside) == 2:
            beachside = ' IS NOT NULL '
            bayside = '= 1 '

        oceanfront = ""
        bayfront = ""
        oceanfrontBayfront = request.form['oceanfrontBayfront']
        
        if int(oceanfrontBayfront) == 0:
            oceanfront = ' = 0 '
            bayfront = ' = 0 '
        elif int(oceanfrontBayfront) == 1:
            oceanfront = ' = 1 '
            bayfront = ' IS NOT NULL '
        elif int(oceanfrontBayfront) == 2:
            oceanfront = ' IS NOT NULL '
            bayfront = ' = 1 '
        elif int(oceanfrontBayfront) == 3:
            oceanfront = ' = 1 '
            bayfront = ' = 1 '

        ac = request.form['ac']
        if ac == 0:
            ac = ' IS NOT NULL '
        else:
            ac = '= ' + ac + ' '
        
        washerDryer = request.form['washerDryer']
        if washerDryer == 0:
            washerDryer = ' IS NOT NULL '
        else:
            washerDryer = '= ' + washerDryer + ' '

        outsideShower = request.form['outsideShower']
        if outsideShower == 0:
            outsideShower = 'IS NOT NULL '
        else:
            outsideShower = '= ' + outsideShower + ' '

        numOfBedrooms = request.form['numOfBedrooms']
        if numOfBedrooms == "":
            numOfBedrooms = ' IS NOT NULL '
        else:
            numOfBedrooms = ' = ' + numOfBedrooms + ' '
        
        numOfBathroom = request.form['numOfBathrooms']
      
        if numOfBathroom == "":
            numOfBathroom = ' IS NOT NULL '
        else:
            numOfBathroom = ' = ' + numOfBathroom + ' '


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       
        
        cursor.execute('SELECT * FROM Property WHERE bbq' + bbq + ' AND pool' + pool + ' AND pets ' + pets\
            + ' AND beachside ' + beachside + ' AND bayside ' + bayside + ' AND numOfBedroom ' + numOfBedrooms\
                 + ' AND numOfBathroom ' + numOfBathroom + ' AND oceanFront ' + oceanfront + ' AND bayFront ' + bayfront, ())
        
         
        # Fetch one record and return result
        property = cursor.fetchall()

        # If account exists in accounts table in out database
        if property:
            return render_template('propertyResults.html', property=property)
        else:
            # Account doesnt exist or username/password incorrect
             flash('Something is incorrect within your query or no properties matching your request exist!', 'message')
            # TODO If time allows, add a message saying that no properties were found, separating out from the error message

    return render_template('searchProperty.html'), property


# This method is used to display ALL data about a property when clicked on
@app.route('/displayPropertyByID/',  methods=['GET', 'POST'])
def displayPropertyByID():
    
   if request.method == 'POST':
        # Create variables for easy access
        propertyID = request.form['propertyID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Property WHERE propertyID = %s', (propertyID,))
        # Fetch one record and return result
        property = cursor.fetchone()
        # If account exists in accounts table in out database
        if property:
            return render_template('propertyDetails.html', property=property)
        else:
             print("dont Exist")
            # Account doesnt exist or username/password incorrect
             flash('Nah fam', 'message')
        return render_template('searchProperty.html')


######################################################## LEASE SECTION ######################################################

# When a user clicks on the "New Lease" button, they are redirected to this page
@app.route('/newLeaseCreation/', methods=['GET', 'POST'])
def newLeaseButton():
    msg=''
    return render_template('newLease.html', msg=msg)


@app.route('/leaseMainPage', methods=['GET', 'POST'])
def leaseMainPage():
    msg = ''
    return render_template('leaseMainPage.html', msg=msg)


# This is where a new Lease will be created
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

                cursor.execute('SELECT leaseID FROM Leases ORDER BY leaseID DESC LIMIT 0,1')

                leaseIDTuple = cursor.fetchone()
                leaseData = leaseIDTuple["leaseID"]
                
                cursor.execute(
                    'INSERT INTO unavailability (startDate, endDate, reason, PropertyID, LeaseID) VALUES (%s, %s, %s, %s, %s)',
                    (StartDate,EndDate,"LeaseRes",PropertyID, leaseData))
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

# This is the page where a user can determine how to search for the lease they are looking for
@app.route('/searchLease/', methods=['GET', 'POST'])
def searchLeasePage():
    return render_template('searchLease.html')

# This method is used to search for a lease by its ID
@app.route('/searchLeaseByID/', methods=['GET', 'POST'])
def searchLeaseByID():
    if request.method == 'POST':
        # Create variables for easy access
        leaseID = request.form['leaseID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Leases.startDate, Leases.endDate, Leases.price, Property.propertyAddress, Property.propertyAddressLine2, Property.propertyState, Property.propertyCity, Property.propertyZip FROM Leases INNER JOIN Property ON Leases.propertyID = Property.propertyID WHERE leaseID = %s', (leaseID,))
        # Fetch one record and return result
        lease = cursor.fetchone()
        leaseArray =[lease]
        # If account exists in accounts table in out database
        if lease:
            return render_template('leaseResults.html', lease=leaseArray)
        else:
            # Account doesnt exist or username/password incorrect
             flash('Either no lease with that information exists, or your information was entered incorrectly, please try again!', 'message')
    return render_template('searchLease.html')

# This method is used to search for a lease by its Status
@app.route('/searchLeaseByStatus/', methods=['GET', 'POST'])
def searchLeaseByStatus():
    if request.method == 'POST':
        # Create variables for easy access
        status = request.form['leaseStatus']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Leases.startDate, Leases.endDate, Leases.price, Property.propertyAddress, Property.propertyAddressLine2, Property.propertyState, Property.propertyCity, Property.propertyZip FROM Leases INNER JOIN Property ON Leases.propertyID = Property.propertyID WHERE leaseStatus = %s', (status,))
        # Fetch one record and return result
        lease = cursor.fetchall()
        print(lease)
        # If account exists in accounts table in out database
        if lease:
            return render_template('leaseResults.html', lease=lease)
        else:
            # Account doesnt exist or username/password incorrect
             flash('There is no user that matches that information, please try again', 'message')
    return render_template('searchLease.html')


# This method is used to search for a lease by the tenantID
@app.route('/searchLeaseByTenant/', methods=['GET', 'POST'])
def searchLeaseByTenant():
    if request.method == 'POST':
        # Create variables for easy access
        tenantID = request.form['tenantID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Leases.startDate, Leases.endDate, Leases.price, Property.propertyAddress, Property.propertyAddressLine2, Property.propertyState, Property.propertyCity, Property.propertyZip FROM Leases INNER JOIN Property ON Leases.propertyID = Property.propertyID WHERE tenantID = %s', (tenantID,))
        # Fetch one record and return result
        lease = cursor.fetchall()
        print(lease)
        # If account exists in accounts table in out database
        if lease:
            return render_template('leaseResults.html', lease=lease)
        else:
            # Account doesnt exist or username/password incorrect
             flash('Either no lease with that information exists, or your information was entered incorrectly, please try again!', 'message')
    return render_template('searchLease.html')


# This method is used to search for a lease by the PropertyID
@app.route('/searchLeaseByProperty/', methods=['GET', 'POST'])
def searchLeaseByProperty():
    if request.method == 'POST':
        # Create variables for easy access
        propertyID = request.form['propertyID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Leases.startDate, Leases.endDate, Leases.price, Property.propertyAddress, Property.propertyAddressLine2, Property.propertyState, Property.propertyCity, Property.propertyZip FROM Leases INNER JOIN Property ON Leases.propertyID = Property.propertyID WHERE Leases.propertyID = %s', (propertyID,))
        # Fetch one record and return result
        lease = cursor.fetchall()
        print(lease)
        # If account exists in accounts table in out database
        if lease:
            return render_template('leaseResults.html', lease=lease)
        else:
            # Account doesnt exist or username/password incorrect
             flash('Either no lease with that information exists, or your information was entered incorrectly, please try again!', 'message')
    return render_template('searchLease.html')

# This method is used to search for a lease by the PropertyID
@app.route('/searchLeaseByAddress/', methods=['GET', 'POST'])
def searchLeaseByAddress():
    if request.method == 'POST':
        # Create variables for easy access
        propertyAddress = request.form['propertyAddress']
        propertyAddress = '%' + propertyAddress + '%'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Leases.startDate, Leases.endDate, Leases.price, Property.propertyAddress, Property.propertyAddressLine2, Property.propertyState, Property.propertyCity, Property.propertyZip FROM Leases INNER JOIN Property ON Leases.propertyID = Property.propertyID WHERE Property.propertyAddress LIKE %s', (propertyAddress,))
        # Fetch one record and return result
        lease = cursor.fetchall()
        print(lease)
        # If account exists in accounts table in out database
        if lease:
            return render_template('leaseResults.html', lease=lease)
        else:
            # Account doesnt exist or username/password incorrect
             flash('Either no lease with that information exists, or your information was entered incorrectly, please try again!', 'message')
    return render_template('searchLease.html')

if __name__ == '__main__':
    app.run()
