# Spotchallenge : DIDI ACOSTA
## Python backend developer test

I did do the project using Django Framework. 

1. Solution implemented for each exercise
2. Project code structure
3. Installation
4. How to run the project

## 1. Solution implemented for each exercise:
>I asumed you run from localhost for testing.

estructura JSON response services develop:
```json
{
    "status": "success",
    "message": "",
    "data": {
        "page": 1,
        "perPage": 10,
        "totalPages": 3,
        "results": [{},{},{}...{}]
    }
}
```
##### - Create an API that has the following endpoints:
- An endpoint to provide a search lookup within the tracks (at least by name, but is
open to any suggestions): I develop the service using Django Rest Framework

Url endpoint: **http://localhost:8000/api/song/**

| Param | Usage |
| ------ | ------ |
| name | Allow to search tracks using their name |
| artistName |  Allow to search tracks using the artist name |
| id |  Allow to search tracks using their id |
| dateReleaseFrom |  Allow to find tracks where their release date is greater than the received param |
| dateReleaseTo |Allow to find tracks where their release date is less than the received param |
| genreName | Allow to search tracks using their genre name |
| top50 | Allow to get the top 50 popularity tracks |
| page | Allow to get the registers paginated, showing 10 rows per page. If this param is not sended, the endpoint will return all the rows. When this param is sended the service will return: page, total pages and rows as results property|
| groupByGenre | Allow to get the tracks grouped by genres. You must to send 1 as value for this param |
>the params can be combined by to do especific filters.
>I Used SQL instead of ORM only for SELECT queries.

- An endpoint that would allow to get the top 50 popularity tracks: 
-- You can use the follow endpoint, using the top50 param equals 1: **http://localhost:8000/api/song/?top50=1**
- An endpoint to remove a track, using a given identifier (defined by you):
--You can use the follow endpoint, using the customId param (wich is autogenered by the application): **http://localhost:8000/api/song/delete/?customId=value**

- An endpoint to add new tracks using ORM:
-- You can use the follow endpoint as a POST request by add new tracks: **http://localhost/api/song**. The service will asign automaticly the value for customId field. I used Django ORM for this endpoint.

> It is important to leave clear than all endpoints require authentication. This project use basic authentication, only username and password, whereby, It is necesary to create a superuser [(see installation)](##Installation) on the application database.

## 2. Project code structure:
I use a standard django project structure:
- song folder: contains the app django witch models.py and views.py files where put database models and services controllers respectively.
- spotchallenge folder: 
     - setting.py: it contains settings params for the project, including database name, authentication type, among other settings parameters.
     - urls.py: it contains url by accesing API song app.
- utilities folder:
     - structure.py: it contains the structure for all services response project.
- createSchemaAndLoadData.py: this script allow create the song.sqlite3 database, get data from the external JSON file and populate the song table.
- requirements.txt: this file contains all depedences required by the project for to work correctly.

## 3. Installation

the project requires Python 3.7.4+ to run.
I sugest to create a virtual enviroment. I recomend Virtualenv 


```sh
pip install virtualenv
virtualenv [enviroment name]
cd [enviroment name]
cd [enviroment name]/scripts
activate
```

clone the repositorio in the folder named: scripts

```sh
cd spotchallenge
pip install -r requirements.txt
```

run the createSchemaAndLoadData.py by to create song.sqlite3, get data from external JSON and populate the database:

```sh
python createSchemaAndLoadData.py
```

run migrate command by to create tables for users authentication using Django framework:

```sh
python manage.py migrate
```
## 4. How to run the project
After to run migrate command, it necesary create superuser by accesing to API song:

```sh
python manage.py createsuperuser
```

run the project by testing endpoints:

```sh
python manage.py runserver
```

I recomend to use tools like Postman by test endpoints.
>Note: It is necesary to pass username and password by accesing endpoints. (I use basic authentication)
