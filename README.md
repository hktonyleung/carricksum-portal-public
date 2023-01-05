# CARRICK SUM PORTAL
> CARRICK SUM PORTAL is a dummy company portal implemented by python, django, javascript and bootstrap. This is initialize made as the capstone project for HarvardX CS50WCS50's Web Programming with Python and JavaScript course. This project was aimed to create a portal for easy maintenance, implement and scale up. 


## Functionality

- Login/Logout (authentication) & Registrations (distribution code from previous project)
- User Profile Page
- TOTP Page
- Seminar Page
  - Booking Page
  - Ticket Page
- Blog Page
- Branch Page
- Address Page
- Cart Page (Under implementation)
- Report Page(accessible only after 2FA authenticate)
- Admin Functions
  - Seminar Management
  - Branch Management
  - Address Management
- Django Admin Functions
  - Modify the database tables

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the project.

```bash
pip install virtualenv
```
```bash
virtualenv vm_env
```

```bash
source vm_env/scripts/activate
```

```bash
pip install -r requirements.txt
```

```bash
python manage.py runserver
```
## Docker Setup
- docker-compose -f docker-compose.prod.yml build 
- docker-compose -f docker-compose.prod.yml up -d

# Account
- using totp as second factor authentication

# Blogs
- using tinymce as WYSIWYG HTML editor

# Branches
- using postgis, geodjango and leaflet.js

# Portal
- using signal to de-couple the announcement creation

# Report
- using cloudinary to host the pdf report, redis/sqs as broker and celery to handle pdf generation

# Search
- using elasticsearch hosted by bonsai.io (cloud based)
- using "Edge N-Grams" for search-as-you-type queries

