# Disability Wiki Project

## Project Members :

> **Pierre Maret** (Professor)

> **Christo El Morr** (Ast. Professor )

> **Rachel da Silveira Gorman** (Ast. Professor )

> **Fabrice MUHLENBACH** (Ast. Professor )

> **Alexandra Creighton** (PhD Candidate)

> **Rediet Tadesse** (MSc Student)

> **Bushra Kundi** (MSc Student)

> **Dhayananth Dharmalingam** (MSc Student)

## Project Overview

Promote the convention and information about disability rights and articles relating experiences from different countries.

## About the Project

The data behind this project is free, open-source linked data that is mainted in **Wikibase** Project:([disabiilty wiki](https://disabilitywiki.univ-st-etienne.fr/wiki/Main_Page)) .
It promotes information about disability rights.

# Application overview

The application is develoepd using `FLASK-RESTPLUS` framework by following MVC architecture (Model-View-Controller).

### Application directory

    .
    ├── application/
    │   ├── main/
    │   │   ├── controller/      # Controllers directory
    │   │   ├── service/         # Services directory
    │   │   ├── component/       # Components directory
    │   │   ├── model/           # Models directory
    │   │   ├── dto/             # Data Transfer object directory
    │   │   ├── config.py        # Application configuration file
    │   │   └── ...
    │   ├── inti.py              # Appliction init file
    ├── disability_core/
    │   ├── service/                # Services directory
    │   ├── message_controller.py   # Message handler
    ├── resources/
    │   ├── uploads/                # Uploaded file directory
    │   ├── classifier_model/       # Classification model directory
    │   ├── error_log/              # Error logs directory
    │   ├── temp_doc/               # Temp document directory
    ├── manage.py                   # Web application starter
    ├── manage_core.py              # Worker application starter
    ├── create_model.py             # Create model file
    ├── user-config.py              # Pywikibot user config
    ├── user-password.py            # Pywikibot user password
    └── ...

> ## **DETAIL**
>
> `controller`
>
> Controller directory contains controller files that manage requests and responses to the application. All the requests and responses are handled in the controller files. Each controller is named by its responsibility. The controller will redirect the request to the corresponding service file and invokes the required method.
>
> `service`
>
> The main application logic is presented in the service files.
>
> `model`
>
> Model classes are presented in this directory. These calsses represents the database tables
>
> `component`
>
> External resources are accessed using component classes. eg: FastTextComponent class helps to access the model.bin.
>
> `dto`
>
> Data transfer objects are created under this directory. eg: UserDto
>
> `config.py [application/main/config.py]`
>
> Important file of the application. The properties should be configured based on the deployment settings.Important properties are Wikibase settings (QID's , PID's), RabbitMQ host name, and MySQL host details. Setup different properties for testing,development and production. Set ENV variable in the system `DISWIKI_SERVER_ENV` to `[dev,test,prod]` to load appropriate settings.
>
> `inti.py [application/inti.py]`
>
> Register all API resources and Namespaces in this file. Controllers should be registered in this file.
>
> `disability core/`
>
> Worker application is registered in this directory. MessageController class will listen to the RabbitMQ messaging broker and invokes the corresponding service method on arrival of new message.
>
> `resources/`
>
> Resource directory contains all uploaded PDF files and documents. Also, it containst he classification model.bin file and training data file. Errors will be logged inside the error_log/ directory.
>
> `manage.py`
>
> This file is the entry point to Web Application.
>
> > ```bash
> >      cmd: python manage.py run // run the application
> >      cmd: python manage.py create_db // create database tables
> >      cmd: python manage.py delete_db // delete the database tables
> > ```
>
> `manage_core.py`
>
> This file is the entry point to Worker Application.
>
> > ```bash
> >     cmd: python manage_core.py run // run the application
> > ```
>
> `create_model.py`
>
> This file is used to create classification model by passing training data file name.
>
> > ```bash
> >     cmd: python create_model.py training_data.txt
> > ```
>
> `user_config.py && user-password.py`
>
> These files are used to configure pywikibot user authentication

The detail overview and the implementation of this Project is described `report.pdf` file in our repository.

## **Deployment**

> `1. Install MySQL`
>
> Install MySQL server and create a Database schema.

> > ```bash
> >     $sudo mysql -u root -p
> >     $password : >> diswikirights
> >     $create database dis_wiki;
> > ```
> >
> > Update the `config.py [application/main/config.py]` file with the appropriate database settings.
>
> `2. Configure NGINX server`
>
> Set a redirection to the web service from nginx reverse proxy server. Add the following settings in /etc/nginx/sites-available/default.
>
> > ```php
> > server{
> >     listen diswiki:5000;
> >     location / {
> >        proxy_pass http://127.0.0.1:8000;
> >        include proxy_params;
> >     }
> > }
> > ```
>
> `3. Install Gunicorn3 server`
>
> Install Gunicorn3 server to run flask server.
>
> > ```bash
> > $sudo apt-get install gunicorn3
> > //TO RUN
> > $sudo gunicorn3 --log-level debug --bind 0.0.0.0:8000 manage:app <-- this is working. not above python 2 commands.
> > $sudo gunicorn3 --log-level debug --bind 0.0.0.0:8000 manage:app --daemon // run with daemon mode - background process
> > $sudo nohup python3 -u ./manage_instance.py run > output.log & // run as deattach process to the current terminal process.
> > tail -f output.log  // To see the output
> > ```
> >
> > We will not run the application directly using Gunicorn server. Instead, we will use supervisor to run Gunicorn server in a managed environment
>
> `4. Install Supervisor`
>
> Supervisor helps to run background process in a managed environment. It will keep monitor the process and log the output. Also, it will restart the process if any situation occurs. Install supervisor and create two UNIT of configurations for `web server` and `worker` porcesses. Check the log files to debug the application.
>
> > ```
> > $sudo apt-get install supervisor
> > ```
> >
> > Create configuration file in `/etc/supervisor/conf.d/`. Supervisor will read configuration from this directory. (/etc/supervisor/conf.d/flask_server.conf)
> >
> > ```php
> > [program:disability_server]
> > environment=HOME="/home/dd07078u/web-application/backend/"
> > directory=/home/dd07078u/web-application/backend/
> > command=/usr/bin/gunicorn3 manage:app -b 0.0.0.0:8000 --log-level debug -t 30
> > autostart=true
> > autorestart=true
> > stderr_logfile=/home/dd07078u/web-application/log/server.err.log
> > stdout_logfile=/home/dd07078u/web-application/log/server.out.log
> >
> > [program:disability_worker]
> > environment=HOME="/home/dd07078u/web-application/backend/"
> > directory=/home/dd07078u/web-application/backend/
> > command=/usr/bin/python3 /home/dd07078u/web-application/backend/manage_instance.py run
> > autostart=true
> > autorestart=true
> > stderr_logfile=/home/dd07078u/web-application/log/worker.err.log
> > stdout_logfile=/home/dd07078u/web-application/log/worker.out.log
> > ```
> >
> > After creating the file, re-read the configuration file and restart the supervisor service.
> >
> > ```bash
> > $sudo supervisorctl reread   //read configuraiton
> > $sudo service supervisor restart // restart service
> > $sudo supervisorctl status  // check status
> > $sudo supervisorctl stop  // stop service
> > ```
>
> `5. Deploy RabbitMQ Docker Image`
> Server and Worker application communicates using RabbitMQ message broker. RabbitMQ must be run in the host machine and the hostname property should be updated in the `config.py`.
>
> > ```yaml
> > version: "3.7"
> >
> > services:
> >   rabbitmq:
> >     image: "rabbitmq:3.6-management-alpine"
> >     volumes:
> >       - ./data:/data
> >     ports:
> >       - 5672:5672
> >       - 15672:15672
> > ```

#### NOTE!!!

Please refer `report.pdf` for more information.

## Stack

- Python 3
- Flask-RestPlus
- React JS- V-17.0.2
- RabbitMQ
- MySQL

## Reference

### Library Reference

**Deploy flask with supervisor** : https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18
