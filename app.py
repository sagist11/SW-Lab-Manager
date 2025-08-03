from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import threading
import time
from ping3 import ping
import psutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sw_labs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    stations = db.relationship('Station', backref='lab', lazy=True, cascade='all, delete-orphan')

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)
    occupied_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    occupied_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    devices = db.relationship('Device', backref='station', lazy=True, cascade='all, delete-orphan')

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(20), nullable=False)  # 'PC' or 'Server'
    ip_address = db.Column(db.String(15), nullable=False)
    os_info = db.Column(db.String(200))
    special_apps = db.Column(db.Text)
    is_online = db.Column(db.Boolean, default=False)
    last_ping = db.Column(db.DateTime)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ping monitoring thread
def ping_devices():
    while True:
        try:
            devices = Device.query.all()
            for device in devices:
                try:
                    result = ping(device.ip_address, timeout=2)
                    device.is_online = result is not None
                    device.last_ping = datetime.utcnow()
                except:
                    device.is_online = False
                    device.last_ping = datetime.utcnow()
            
            db.session.commit()
        except Exception as e:
            print(f"Error in ping monitoring: {e}")
        
        time.sleep(30)  # Ping every 30 seconds

# Routes
@app.route('/')
def index():
    labs = Lab.query.all()
    return render_template('index.html', labs=labs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/lab/<int:lab_id>')
def lab_detail(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    return render_template('lab_detail.html', lab=lab)

@app.route('/station/<int:station_id>')
def station_detail(station_id):
    station = Station.query.get_or_404(station_id)
    return render_template('station_detail.html', station=station)

@app.route('/occupy_station/<int:station_id>', methods=['POST'])
@login_required
def occupy_station(station_id):
    station = Station.query.get_or_404(station_id)
    
    if station.is_occupied:
        flash('Station is already occupied')
        return redirect(url_for('station_detail', station_id=station_id))
    
    station.is_occupied = True
    station.occupied_by = current_user.id
    station.occupied_at = datetime.utcnow()
    db.session.commit()
    
    flash('Station occupied successfully')
    return redirect(url_for('station_detail', station_id=station_id))

@app.route('/release_station/<int:station_id>', methods=['POST'])
@login_required
def release_station(station_id):
    station = Station.query.get_or_404(station_id)
    
    if not station.is_occupied:
        flash('Station is not occupied')
        return redirect(url_for('station_detail', station_id=station_id))
    
    if station.occupied_by != current_user.id and not current_user.is_admin:
        flash('You can only release stations you occupied')
        return redirect(url_for('station_detail', station_id=station_id))
    
    station.is_occupied = False
    station.occupied_by = None
    station.occupied_at = None
    db.session.commit()
    
    flash('Station released successfully')
    return redirect(url_for('station_detail', station_id=station_id))

# Admin routes
@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    labs = Lab.query.all()
    stations = Station.query.all()
    devices = Device.query.all()
    users = User.query.all()
    
    return render_template('admin_panel.html', labs=labs, stations=stations, devices=devices, users=users)

@app.route('/admin/lab/add', methods=['GET', 'POST'])
@login_required
def add_lab():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        location = request.form['location']
        
        lab = Lab(name=name, description=description, location=location)
        db.session.add(lab)
        db.session.commit()
        
        flash('Lab added successfully')
        return redirect(url_for('admin_panel'))
    
    return render_template('add_lab.html')

@app.route('/admin/station/add', methods=['GET', 'POST'])
@login_required
def add_station():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        lab_id = request.form['lab_id']
        
        station = Station(name=name, description=description, lab_id=lab_id)
        db.session.add(station)
        db.session.commit()
        
        flash('Station added successfully')
        return redirect(url_for('admin_panel'))
    
    labs = Lab.query.all()
    return render_template('add_station.html', labs=labs)

@app.route('/admin/device/add', methods=['GET', 'POST'])
@login_required
def add_device():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        device_type = request.form['device_type']
        ip_address = request.form['ip_address']
        os_info = request.form['os_info']
        special_apps = request.form['special_apps']
        station_id = request.form['station_id']
        
        device = Device(
            name=name, device_type=device_type, ip_address=ip_address,
            os_info=os_info, special_apps=special_apps, station_id=station_id
        )
        db.session.add(device)
        db.session.commit()
        
        flash('Device added successfully')
        return redirect(url_for('admin_panel'))
    
    stations = Station.query.all()
    return render_template('add_device.html', stations=stations)

@app.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_admin = 'is_admin' in request.form
        
        user = User(
            username=username, email=email,
            password_hash=generate_password_hash(password),
            is_admin=is_admin
        )
        db.session.add(user)
        db.session.commit()
        
        flash('User added successfully')
        return redirect(url_for('admin_panel'))
    
    return render_template('add_user.html')

# API routes for AJAX updates
@app.route('/api/device_status')
def device_status():
    devices = Device.query.all()
    status_data = []
    
    for device in devices:
        status_data.append({
            'id': device.id,
            'name': device.name,
            'is_online': device.is_online,
            'last_ping': device.last_ping.isoformat() if device.last_ping else None
        })
    
    return jsonify(status_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if none exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@swlabs.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    
    # Start ping monitoring in a separate thread
    ping_thread = threading.Thread(target=ping_devices, daemon=True)
    ping_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)