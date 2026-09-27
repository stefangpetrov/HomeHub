# HomeHub

HomeHub is a web-based real estate platform developed as a bachelor's diploma project at the Technical University of Sofia.

The platform allows users to browse real estate properties, search and filter listings, save favorite properties, send inquiries, and create saved searches with automatic notifications. Agents and administrators can manage property listings according to their assigned roles.

## Features

* User registration and authentication
* Role-based access control

  * User
  * Agent
  * Admin
* Property listing and detailed property pages
* Property search and filtering
* Property creation, editing, and deletion
* Property image management
* Favorites
* Inquiries between users and property agents
* Saved searches
* Automatic notifications for matching properties
* Pagination
* REST API for property management
* Swagger / OpenAPI documentation
* Automated tests

## Technologies

* Python 3.13
* Django 6.1
* PostgreSQL 18
* Django REST Framework
* drf-spectacular
* Bootstrap 5
* HTML / CSS / JavaScript
* Git / GitHub

## Project Structure

```text
Homehub/
├── HomeHub/          # Project configuration
├── users/            # Authentication and user roles
├── properties/       # Property management and REST API
├── favorites/        # Favorite properties
├── inquiries/        # Property inquiries
├── saved_searches/   # Saved searches and notifications
├── core/             # Home page and shared functionality
├── static/           # Static files
├── media/            # Uploaded property images
└── manage.py
```

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:stefangpetrov/HomeHub.git
cd Homehub
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
DB_NAME=homehub
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5433
```

Adjust the database credentials according to your local PostgreSQL installation.

### 5. Create the database

Create a PostgreSQL database named:

```text
homehub
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create an administrator

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

## API Documentation

The REST API is documented using Swagger/OpenAPI.

When the development server is running, the documentation is available at:

```text
http://127.0.0.1:8000/api/docs/
```

## Testing

The project contains automated tests covering models, views, permissions, and core application behavior.

Run all tests with:

```bash
python manage.py test
```

## Database

HomeHub uses PostgreSQL as its relational database.

The main entities include:

* Users
* Properties
* Property Images
* Favorites
* Inquiries
* Saved Searches
* Notifications

Relationships between these entities enforce data consistency and support the main functionality of the platform.

## Project Status

HomeHub was developed as a bachelor's diploma project for the Technical University of Sofia.

The core functionality, REST API, role-based access control, automated testing, and user-facing interface are implemented.
