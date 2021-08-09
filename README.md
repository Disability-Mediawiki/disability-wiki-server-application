# Disability Wiki Project
## Project Members : 

>**Pierre Maret**
>**Christo El Morr**
>**Rachel da Silveira Gorman**
>**Fabrice MUHLENBACH**
>**Alexandra Creighton**
>**Rediet Tadesse**
>**Bushra Kundi**
>**Dhayananth Dharmalingam**


## Project Overview 
 Promote the convention and information about disability rights and articles relating experiences from different countries.

## About the Project

The data behind this project is free, open-source linked data that is mainted in **Wikibase** Project:([disabiilty wiki](https://disabilitywiki.univ-st-etienne.fr/wiki/Main_Page)) .
It promotes information about disability rights.

# Application overview 
The application is develoepd using `FLASK-RESTPLUS` framework by following MVC architecture (Model-View-Controller). 
 ### Application directory
    .
    ├── application
    │   ├── main                
    │   │   ├── controller/      # Controllers directory
    │   │   ├── service/         # Services directory   
    │   │   ├── component/       # Components directory    
    │   │   ├── model/           # Models directory  
    │   │   ├── dto/             # Data Transfer object directory  
    │   │   ├── config.py        # Application configuration file  
    │   │   └── ...       
    │   ├── inti.py              # Appliction init file 
    ├── disability_core
    │   ├── service/                # Services directory
    │   ├── message_controller.py   # Message handler 
    ├── resources
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

    
> ## **CLIENT-WORKER**
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
> Important file of the application. The properties should be configured based on the deployment settings.Important properties are Wikibase settings (QID's , PID's), RabbitMQ host name, and MySQL host details.   
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
>>  ```
>>      cmd: python manage.py run // run the application
>>      cmd: python manage.py create_db // create database tables
>>      cmd: python manage.py delete_db // delete the database tables
>>  ``` 
>
> `manage_core.py` 
>   
> This file is the entry point to Worker Application. 
>>  ```
>>      cmd: python manage_core.py run // run the application
>>  ``` 
>
> `create_model.py` 
>   
> This file is used to create classification model by passing training data file name. 
>>  ```
>>      cmd: python create_model.py training_data.txt
>>  ``` 
>
> `user_config.py && user-password.py` 
>   
> These files are used to configure pywikibot user authentication 

The detail overview and the implementation of this Project is described `report.pdf` file in our repository.




## How to get started with the Project
 
 1. To run the program Java 11 or greater version must be installed in the computer
 2. Download the Application file from Git repositories (front-app & server-routing-client repositories need to be downloaded) (Here is the link : [click-here](https://github.com/ujm-cloud-computing-open))

 3. edit configuration files in server-routing-client as follow.
    * aws.access.key: your AWS Access key. (Ex: `AWSDZXCSD23`)
    * aws.secret.key: your AWS SAecret key. (Ex: `AWSDZXCSD23`)
    * aws.session: your AWS Access session. (Ex: `some long string`)
    * aws.queue.number_list_sender: your SQS queue name for number list `request`. 
    * aws.queue.number_list_reciever: your SQS queue name for number list `response`. 
    * aws.s3.bucket.image_list.name: Your AWS S3 Bucket name for image storing.
    * aws.s3.bucket.image_list.original.folder: Your AWS S3 Bucket **folder** name for **orignal** image storing
    * aws.s3.bucket.image_list.edited.folder: Your AWS S3 Bucket **folder** name for **edited** image storing

 5. Import the project to Eclipse as Maven Project. (Here is the link : [click-here](https://www.eclipse.org/downloads/packages/installer))
 7. Run the java application
 8. Run the front-app (see below for instruction)
 9. In the User interface there are Specific buttons  which allows to see what the application is performing. 



#### NOTE!!!
> Please refer `report.pdf` for more information. 

## Stack
* Python 3
* Flask-RestPlus
* React JS- V-17.0.2

## Reference 
 ### Library Reference 
**Java AWS SDK** : https://aws.amazon.com/sdk-for-java/

**Configuration file** : https://www.codejava.net/coding/reading-and-writing-configuration-for-java-application-using-properties-class

**Spring boot** : https://spring.io/projects/spring-boot

**Jackson.jar** : https://github.com/FasterXML/jackson

 
## ANGULAR SPECIFIC SUPPORT

Your are required to install NODE JS and Angular CLI in local computer to proceed with below steps. 
(How to install NODE JS : [click-here](https://phoenixnap.com/kb/install-node-js-npm-on-windows))
(How to install Angular CLI: [click-here](https://cli.angular.io/))

## Initiate node package
Run `npm install` in the root folder.
## Start the application
Run `ng serve` to start the application in local environment.

# Front-App For Cloud Computing Project

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 8.3.24.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
