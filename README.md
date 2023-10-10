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
- Docker compose (optional)

## 1. Run project:
### 1.1 Run with docker:
- create .env file
- Build: `docker-compose -f docker-compose.yml build`
- Run server: `docker-compose up`
- Link: http://localhost:8000/
- Run migrate: `docker exec -it django_server python manage.py migrate`

### 1.1 Run without docker:
- create .env file
- Run command: `python manage.py runserver`
- Link: http://localhost:8000/
   Run migrate: `python manage.py migrate`
