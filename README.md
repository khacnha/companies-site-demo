# Django Project

**Background**
```
Create a simple web page, using Django where a user can see a list of companies with links to companies’ profiles. 

When the link is clicked, an email will be be sent to an admin user to approve the download. 

Once the request is approved, a user will get a pre-signed url of a company profile file they requested through email. 

You don’t have to actually create a s3 bucket and write the code assuming 
there already is one
```

## Requirement:
- Python v3.11
- Django v4.2.1

## Developer:
- Creating a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
- Docker (optional)
- Install pylint and pylint-django

## 1. Run project:
### 1.1 Run with docker:
- copy `.env.example` file to `.env` file and update the configuration.
- Build: `docker-compose -f docker-compose.yml build`
- Run server: `docker-compose up`
- Run migrate: `docker exec -it django_server python manage.py migrate`
- Create superuser: `docker exec -it django_server python manage.py createsuperuser --username=admin --email=admin@gmail.com`
- Admin page: http://localhost:8000/admin

### 1.1 Run without docker:
- copy `.env.example` file to `.env` file and update the configuration.
- Install requirements.txt: `pip install -r requirements.txt`
- Run command: `python manage.py runserver`
- Run migrate: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser --username=joe --email=joe@example.com`

## 2. Check in browser:
- Webiste page: http://localhost:8000/
- Admin page: http://localhost:8000/admin

## 3. Testing:
- Run command in docker: `docker exec -it django_server python manage.py test`
- Or without docker: `python manage.py test`

## 4. Mailhog for development(only docker):
- Website to check mail in local: `http://localhost:19802/`

