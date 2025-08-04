# SW Labs Management System

A comprehensive laboratory management system for software development labs, built with Flask and featuring file-based storage.

## Features

- **Lab Management**: Create and manage multiple laboratories
- **Station Management**: Track individual workstations within labs
- **Device Monitoring**: Monitor PCs and servers with real-time ping status
- **User Management**: Admin and regular user roles with authentication
- **File-Based Storage**: Data stored in JSON files for easy backup and portability
- **Real-time Status**: Live device status monitoring
- **Responsive UI**: Modern Bootstrap-based interface

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd SW-Lab-Manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Access the application**
   - Open your browser and go to: `http://localhost:5000`
   - Default admin credentials: `admin` / `admin123`

## File-Based Storage

The system now uses JSON files for data storage instead of SQLite database:

- **`data/users.json`**: User accounts and authentication data
- **`data/labs.json`**: Laboratory information
- **`data/stations.json`**: Workstation data within labs
- **`data/devices.json`**: Device information and status

### Benefits of File-Based Storage

- **Easy Backup**: Simply copy the `data/` folder to backup all data
- **Portable**: Move data between systems by copying JSON files
- **Human Readable**: JSON files can be easily viewed and edited
- **Version Control Friendly**: JSON files work well with Git
- **No Database Setup**: No need to install or configure databases

### Data Migration

If you have existing data in the SQLite database, you can migrate it to JSON files:

```bash
python migrate_to_files.py
```

This will create the `data/` directory with JSON files containing your existing data.

## System Architecture

### Core Components

- **Flask Web Framework**: Backend API and web interface
- **Flask-Login**: User authentication and session management
- **Bootstrap 5**: Modern responsive UI
- **ping3**: Network device monitoring
- **JSON Storage**: File-based data persistence

### Data Structure

```
data/
├── users.json      # User accounts
├── labs.json       # Laboratories
├── stations.json   # Workstations
└── devices.json    # Devices (PCs/Servers)
```

## Usage

### Admin Panel

Access the admin panel to manage:
- **Labs**: Create and configure laboratories
- **Stations**: Add workstations to labs
- **Devices**: Configure PCs and servers with IP addresses
- **Users**: Create and manage user accounts

### Regular Users

Regular users can:
- View lab and station information
- Occupy and release stations
- Monitor device status
- View their activity history

### Device Monitoring

The system automatically pings devices every 30 seconds to check their online status. Device status is displayed in real-time on the web interface.

## Troubleshooting

### Login Issues

If you experience login problems:

1. **Clear browser cache and cookies**
2. **Check that the data/users.json file exists**
3. **Verify admin credentials**: `admin` / `admin123`
4. **Restart the application**

### Device Monitoring Issues

If devices show as offline:

1. **Check IP addresses** are correct in device configuration
2. **Verify network connectivity** between the server and devices
3. **Check firewall settings** that might block ping requests
4. **Ensure devices are powered on** and connected to the network

### File Storage Issues

If data files are corrupted:

1. **Backup the data/ directory** before making changes
2. **Check JSON syntax** in the data files
3. **Restore from backup** if needed
4. **Run the migration script** to recreate files

## Development

### Adding New Features

1. **Backend**: Add routes in `app.py`
2. **Frontend**: Create templates in `templates/`
3. **Styling**: Update `static/css/style.css`
4. **JavaScript**: Modify `static/js/app.js`

### Data Model Changes

When modifying data structures:

1. **Update the JSON file schemas**
2. **Modify the file-based storage functions** in `app.py`
3. **Update the migration script** if needed
4. **Test with sample data**

## Security Considerations

- **Password Hashing**: All passwords are hashed using Werkzeug's security functions
- **Session Management**: Flask-Login handles secure session management
- **Input Validation**: All user inputs are validated and sanitized
- **File Permissions**: Ensure data files have appropriate read/write permissions

## Backup and Recovery

### Regular Backups

```bash
# Backup all data
cp -r data/ backup/data_$(date +%Y%m%d_%H%M%S)/

# Restore from backup
cp -r backup/data_YYYYMMDD_HHMMSS/* data/
```

### Data Export

You can export data to CSV format for external analysis:

```bash
python export_to_csv.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the data files for corruption
3. Check the application logs for error messages
4. Create an issue in the project repository

## Changelog

### Version 2.0
- **NEW**: File-based storage system (JSON)
- **FIXED**: Login loading issue
- **IMPROVED**: Better error handling
- **ADDED**: Data migration script
- **ENHANCED**: Backup and recovery procedures

### Version 1.0
- Initial release with SQLite database
- Basic lab and station management
- Device monitoring functionality
- User authentication system