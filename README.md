# SW Labs Management System

A comprehensive web application for managing and monitoring software development labs, stations, and devices. Built with Python Flask and modern web technologies.

## Features

### Core Functionality
- **Lab Management**: Create and manage multiple labs with locations and descriptions
- **Station Management**: Organize stations within labs with occupancy tracking
- **Device Monitoring**: Monitor PCs and servers with real-time ping status
- **User Management**: User authentication with admin privileges
- **Occupancy System**: Users can occupy and release stations
- **Real-time Status**: Live monitoring of device connectivity

### Admin Features
- **Complete CRUD Operations**: Add, edit, and remove labs, stations, devices, and users
- **System Overview**: Dashboard with statistics and system health
- **User Management**: Create users with different privilege levels
- **Device Configuration**: Configure device types, IP addresses, and special applications

### User Features
- **Station Reservation**: Occupy and release stations
- **Status Monitoring**: View real-time device status
- **Lab Navigation**: Browse labs and stations with detailed information
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (file-based)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **Monitoring**: ping3 library for device connectivity
- **Authentication**: Flask-Login

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd sw-labs-management
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Default admin credentials: `admin` / `admin123`

## Database Structure

The application uses SQLite with the following main entities:

### Labs
- ID, Name, Description, Location, Created Date
- Contains multiple stations

### Stations
- ID, Name, Description, Lab ID, Occupancy Status
- Contains multiple devices (PCs/Servers)

### Devices
- ID, Name, Type (PC/Server), IP Address, OS Info, Special Apps
- Online/Offline status with ping monitoring

### Users
- ID, Username, Email, Password Hash, Admin Status
- Authentication and authorization

## Usage Guide

### For Administrators

1. **Login with admin credentials**
   - Username: `admin`
   - Password: `admin123`

2. **Add Labs**
   - Go to Admin Panel → Add Lab
   - Provide lab name, location, and description

3. **Add Stations**
   - Go to Admin Panel → Add Station
   - Select the lab and provide station details

4. **Add Devices**
   - Go to Admin Panel → Add Device
   - Configure device type, IP address, and special applications

5. **Manage Users**
   - Go to Admin Panel → Add User
   - Create users with appropriate privilege levels

### For Regular Users

1. **Browse Labs**
   - View all available labs on the home page
   - Click on labs to see detailed information

2. **View Stations**
   - Navigate through labs to see stations
   - View device status and information

3. **Occupy Stations**
   - Click "Occupy" on available stations
   - You'll be responsible for the station until you release it

4. **Release Stations**
   - Click "Release" on occupied stations
   - Only you or an admin can release your occupied stations

## Configuration

### Environment Variables
Create a `.env` file in the project root for custom configuration:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///sw_labs.db
FLASK_ENV=development
```

### Ping Monitoring
The system automatically pings devices every 30 seconds to check connectivity. You can modify this interval in `app.py`:

```python
time.sleep(30)  # Change this value to adjust ping frequency
```

## API Endpoints

### Public Endpoints
- `GET /` - Home page with labs overview
- `GET /lab/<id>` - Lab details
- `GET /station/<id>` - Station details
- `GET /api/device_status` - Device status API

### Protected Endpoints
- `POST /occupy_station/<id>` - Occupy a station
- `POST /release_station/<id>` - Release a station
- `GET /admin` - Admin panel (admin only)
- `POST /admin/lab/add` - Add new lab (admin only)
- `POST /admin/station/add` - Add new station (admin only)
- `POST /admin/device/add` - Add new device (admin only)
- `POST /admin/user/add` - Add new user (admin only)

## Security Features

- **Password Hashing**: All passwords are securely hashed using Werkzeug
- **Session Management**: Flask-Login handles user sessions
- **Admin Protection**: Admin routes are protected with privilege checks
- **CSRF Protection**: Forms include CSRF protection
- **Input Validation**: Server-side validation for all inputs

## Monitoring and Maintenance

### Database Backup
The SQLite database is stored in `sw_labs.db`. Regular backups are recommended:

```bash
cp sw_labs.db sw_labs_backup_$(date +%Y%m%d).db
```

### Logs
Application logs are printed to the console. For production, consider using a proper logging system.

### Performance
- Device ping monitoring runs in a separate thread
- Database queries are optimized with SQLAlchemy
- Static assets are served efficiently

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `app.py`: `app.run(port=5001)`

2. **Database errors**
   - Delete `sw_labs.db` and restart the application
   - The database will be recreated automatically

3. **Ping failures**
   - Ensure devices have valid IP addresses
   - Check network connectivity
   - Verify firewall settings

4. **Permission errors**
   - Ensure the application has write permissions for the database file
   - Check file system permissions

### Support
For issues and questions:
1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure Python version is 3.7 or higher

## Development

### Adding New Features
1. Create new routes in `app.py`
2. Add corresponding templates in `templates/`
3. Update static files as needed
4. Test thoroughly before deployment

### Customization
- Modify `static/css/style.css` for custom styling
- Update `static/js/app.js` for additional functionality
- Customize templates in the `templates/` directory

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This is a development system. For production use, consider:
- Using a production-grade database (PostgreSQL, MySQL)
- Implementing proper logging
- Adding HTTPS support
- Setting up monitoring and alerting
- Regular security updates