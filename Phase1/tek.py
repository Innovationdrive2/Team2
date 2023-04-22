
from flask import Flask, request, redirect, url_for, flash, session
from flask.templating import render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import netmiko

application = Flask(__name__)

# adding configuration for using a sqlite database
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:Admin_123@localhost:3306/tek'
application.secret_key = 'dummy'

# Creating an SQLAlchemy instance
db = SQLAlchemy(application)
migrate = Migrate(application, db)

# Creating an engine for ping.
e = create_engine("mysql+mysqlconnector://admin:Admin_123@localhost:3306/id", pool_pre_ping=True)
e = create_engine("mysql+mysqlconnector://admin:Admin_123@localhost:3306/id", pool_recycle=300)
e = create_engine("mysql+mysqlconnector://admin:Admin_123@localhost:3306/id", pool_size=10, max_overflow=20)

# Models
class Cube(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)	
    cube_management_IP = db.Column(db.String(20), unique=True, nullable=True)
    username = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(20), nullable=True)
    enable_password = db.Column(db.String(20), nullable=True)
    comments = db.Column(db.String(20), nullable=True)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Cube: {self.cube_management_IP}"


with application.app_context():
    db.create_all()


@application.route('/')
def landing_page():
    return render_template('login.html')

@application.route('/index')
def index():
    return render_template('index.html')


@application.route('/home')
def home():
    cubes = Cube.query.all()
    # Pass the cubes data to the template
    return render_template('home.html', cubes=cubes)


@application.route('/submit', methods=['POST'])
def submit_form():
    try:
        # extract form data from the request object
        cube_ip = request.form['cube_ip']
        username = request.form['username']
        password1 = request.form['pwd1']
        password2 = request.form['pwd2']
        comments = request.form['comments']

        # save the form data to the database
        # use your database library or ORM to save the data
        # for example, with SQLAlchemy:
        cube = Cube(cube_management_IP = cube_ip,
                    username = username,
                    password = password1,
                    enable_password = password2,
                    comments = comments)
        print(cube)
        db.session.add(cube)
        db.session.commit()

        # add a flash message indicating success
        flash('Cube added successfully!', 'success')

        # redirect to the home page
        return redirect(url_for('home'))

    except Exception as e:
        # add a flash message indicating the error
        try:
            error = e.orig.args
        except AttributeError as e:
            error = "please enter valid input"
        flash(f'Error submitting form: {error}', 'danger')

        # redirect back to the same page
        return redirect(request.referrer)


@application.route('/connect', methods=['POST'])
def connect_cube():
    # Get the data from the request
    form_data = request.form
    # Return a response
    try:
        connection = netmiko.ConnectHandler(device_type='cisco_ios',
                                            ip=form_data['cube_ip'],
                                            username=form_data['username'],
                                            password=form_data['password'],
                                            secret=form_data['enable_password'])
        connection.enable()
        if connection:
            print(connection)
        output = connection.send_command("show run")
        output_1 = connection.send_command('show cube status')
        output_2 = connection.send_command('show dial-peer voice summary')
        connection.disconnect()
        return render_template("cube.html", output=output, output1=output_1, output2=output_2)
    except ConnectionRefusedError as e:
        message = e.strerror
        return render_template("cube.html", message=message)

@application.route('/delete_cube/<int:cube_id>', methods=['POST'])
def delete_cube(cube_id):
    if request.form['delete'] == 'yes':
        # Delete the cube from the database
        Cube.query.filter_by(id=cube_id).delete()
        db.session.commit()
        flash('Cube deleted successfully!', 'success')
    # Redirect to the previous page
    return redirect(request.referrer)

@application.route("/cube", methods=['POST'])
def cube():
    form_data = request.form
    # Return a response
    try:
        connection = netmiko.ConnectHandler(device_type='cisco_ios',
                                            ip=form_data['cube_ip'],
                                            username=form_data['username'],
                                            password=form_data['enable_password'],
                                            secret=form_data['enable_password'])
        connection.enable()
        output = connection.send_command("show run")
        output1 = connection.send_command('show cube status')
        output2 = connection.send_command('show version')
        output3 = connection.send_command('show cdp neighbors')
        output4 = connection.send_command('show cdp neighbors detail')
        output5 = connection.send_command('Show interface |  s i address')
        output6 = connection.send_command('Show ip interface brief')
        output7 = connection.send_command('Show dial-peer voice summary')
        output8 = connection.send_command('Show dial-peer voip keepalive status')
        output9 = connection.send_command('Show run | s i voice')
        output10 = connection.send_command('Show run | s i license')
        output11 = connection.send_command('Show run | s i ip route')
        output12 = connection.send_command('Show run | s i name-server')
        output13 = connection.send_command('Show run | s i hostname')
        output14 = connection.send_command('who')
        output15 = connection.send_command('show udp ')
        output16 = connection.send_command('show tcp brief')
        output17 = connection.send_command('show sip-ua connection tcp tls brief')
        output18 = connection.send_command('show dial-peer voice summary')
        output19 = connection.send_command('show dial-peer voip keepalive status')
        output20 = connection.send_command('show crypto pki certificates')
        output21 = connection.send_command('Show run | s i voice class codec')
        output22 = connection.send_command('Show run | s i voice class tenant')
        output23 = connection.send_command('Show run | s i voice service voip')
        output24 = connection.send_command('Show run | s i voice class sip-profile')
        output25 = connection.send_command('Show run | s i dial-peer voice')
        output26 = connection.send_command('Show run | s i voice transl')
        output27 = connection.send_command('Show sip-ua service')
        lines = output1.splitlines()

        if len(lines) >= 2:
            output_1 = lines[0] + '\n' + lines[1]
        connection.disconnect()
        return render_template("Monitoring.html", output=output, cube=output_1, version=output2, cdp1=output3, cdp2=output4, MAC=output5, interface=output6,dialpeer1=output7, dialpeer2=output8, license=output10, Routing=output11, DNS=output12, Hostname=output13, linevty=output14, tls2=output17, udp=output15, tcp=output16, Options1=output19, options2=output18, certificate=output20, voip=output23, codec=output21, Dialpeer=output25, Profile=output24, Translation=output26, Tenant=output22, service=output27)
    except ConnectionRefusedError as e:
        message = e.strerror
        return render_template("Monitoring.html", message=message)


@application.route("/Troubleshooting")
def Troubleshooting():
    

    connection = netmiko.ConnectHandler(device_type='cisco_ios', ip="172.16.29.122", username="Admin" , password="tekV1z10n", secret="tekV1z10n")
    connection.enable()
    output11 = connection.send_command('Show voice call active brief')

    connection.disconnect()

    return render_template("troubleshooting.html", DialpeerMatch=output11)

@application.route("/logout", methods=['POST'])
def logout():
    session.clear()
    # Redirect the user to the login page
    return redirect(url_for('landing_page'))


if __name__ == '__main__':
    application.run(debug= True, host='0.0.0.0')
