# [**www.patrick-sheehan.com**](patrick-sheehan.com)

# My Family Cookbook

My Family Cookbook is a web application that helps connect my extended family that is spread out across the country. Anyone can create an account and start cataloging recipes for all to see. During the COVID-19 crisis this website has emboldened family connections, and sparked recipe sharing that spans thousands of miles. As an added side effect, recipes that are over 90 years old have been gathered and cataloged into a digital vault.

![My Family Cookbook Logo](https://raw.githubusercontent.com/Pts19/FlaskBlog/Attempt/familycookbloglogo.png)

## Table of contents
* [Features](#features)
* [Technologies](#technologies)
* [Website Hosting](#website-hosting)
* [Retrospective](#retrospective)
* [Contact](#contact)

## Features

* Secure and simplistic **account creation** and **management**.
  * Passwords and email stored securely using [**Flask-Bcrypt**](https://flask-bcrypt.readthedocs.io/en/latest/). 
    * Stored using an extremely secure **hashing algorithm** that is only used after **salting** the sensitive information.
* Passwords can be reset using **email verification**, a **secure token**, and **GMail API**.
* Ability to **Create** posts that consist of:
  * Meal Title, Meal Type, Main Ingredient, and instructions.
* Ability to **Read** posts and their information. 
* Ability to **Update** posts and their information.
* Ability to **Delete** posts and their information.
  * All posts are stored and cataloged in a Object Relational Database in the Python SQL toolkit called [**SQLAlchemy**](https://www.sqlalchemy.org/).
* There are Quicklinks that can be used to display and **sort the database** by:
  * My personal Top 5 favorite dishes at any given moment.
  * Main Ingredient type -> Chicken, Beef, Pork, Pasta, etc..
  * Dished traditionally eaten for Breakfast or Dinner.

## Technologies
- [**Flask-Bcrypt**](https://flask-bcrypt.readthedocs.io/en/latest/) - Great security for sensitive data.
- [**certifi**](https://pypi.org/project/certifi/) -Mozilla’s carefully curated collection of Root Certificates for validating the trustworthiness of SSL certificates while verifying the identity of TLS hosts.
- [**Flask**](https://palletsprojects.com/p/flask/) - The bread and butter of this project. Flask is a lightweight WSGI web-app framework that is simply to learn and implement.
- [**Jinja2**](https://jinja.palletsprojects.com/en/2.11.x/) - Jinja is a modern and designer-friendly templating language for Python, modelled after Django’s templates. 

- [**SQLAlchemy**](https://www.sqlalchemy.org/) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

- [**Bootstrap**](https://getbootstrap.com/) - Provides a quick startup to build a responsive and simplistic web-app that implements elements in HTML/Jinja2/CSS. 

- [**Werkzeug**](https://werkzeug.palletsprojects.com/en/1.0.x/) - Werkzeug is a comprehensive WSGI web application library.

All of these packages can be installed using [pip](https://pip.pypa.io/en/stable/) and my [**requirements**](https://github.com/Pts19/FlaskBlog/blob/Attempt/req.txt) test file.
```bash
pip install -r req.txt
```


## Website Hosting
- **Domain name** was purchased using [**namecheap.com**](www.namecheap.com)
- **Cloud Hosted** using [**Linode.com**](https://www.linode.com/) on a Ubuntu based virtual machine.
- **WSGI application server** [**GUnicorn**](https://gunicorn.org/) - GUnicorn handles everything that happens in-between the web server and the web application. 
- Web Sever [**Nginx**](https://www.nginx.com/) - This server handles **requests** and the general **domain logic**, plus the complicated **HTTPs connections**.

## Retrospective
- Must flesh out deaper CSS and HTML/Jinja2 markup skills. Too relient on BootStrap to manage fullstack apps.
- Focus on commenting new code right as I write it. Old functions are messy and hard to comprehend without good comments.
- User Interface may be too simplistic and limited as I try to scale web-app to include more members.


## Contact
**Patrick Sheehan** -> [**patricksheehancs@gmail.com**](patricksheehancs@gmail.com)

[**www.patrick-sheehan.com**](www.patrick-sheehan.com)

## License
[MIT](https://choosealicense.com/licenses/mit/)
