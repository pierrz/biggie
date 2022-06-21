# biggie
<br>
Biggie is a tool to quickly get data from (external) APIs into a Mongo database, 
and have it exposed/searchable via a dedicated new API.

It is a Docker setup with 3 main containers based on Spark, FastAPI and Mongo.
Additional containers can be setup for Mongo Express and Nginx.

Currently set up with an API harvester fine-tuned for the [Marvel API](https://developer.marvel.com).

<br>


### Installation
You have to create the `.env` environment file, most important including your Marvel API keys.
If necessary, update the `docker-compose.main.yml` file to change the common `volumes` variable.

*NB: For all these required files, you'll find `xxxxxx.example` sample files ready to adapt.*

Then eventually pull the docker images ...
```
docker pull ghcr.io/pierrz/biggie_pyspark_img:latest
docker pull ghcr.io/pierrz/biggie_harvester_img:latest
docker pull ghcr.io/pierrz/biggie_api_img:latest
```

... and test that everything works as expected
```
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml up pyspark_test harvester_test api_test
OR
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml --profile test up
```
<br>

### Run
#### Data acquisition and load
```
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml --profile import_data up
```
This command will spin up the Harvester and Spark containers to:

  - download all the data from the Marvel characters API
  - load it into Mongo

<br>

#### API container
Just to have the FastAPI container up
```
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml up api_prod
```

<br>

#### Monitoring
Spin up the Mongo-Express container to access the Mongo UI
```
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml --profile monitoring up
```

<br>

#### The whole shebang
```
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml --profile api --profile import_data --profile test --profile monitoring up
```

<br>

### Nginx deployment (API container only)
In this configuration, you need to have the necessary sub-domains setup on your domain provider side. 
You also need Nginx installed on the host machine.
<br>

Then create the required files and change the `volumes` path accordingly in the `compose` files.
The `nginx` configuration files are:
- `conf/nginx/certificate.json`
- `conf/nginx/app_docker.conf`
- `conf/nginx/monitor_docker.conf`
<br>

Finally run the `docker-compose` command with the `live_prod` profile:
```
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml --profile live_prod up
```
<br>



### Local URLs

[API docs](http://localhost:8000/docs)

API - Results full list
- [sorted by comics number](http://localhost:8000/api/comics_per_characters?sort_column=comics_available)
- [sorted by name](http://localhost:8000/api/comics_per_characters?sort_column=name)

API - [WIP] Paginated results
- [sorted by comics number](http://localhost:8000/api/comics_per_characters/paginated?sort_column=comics_available)
- [sorted by name](http://localhost:8000/api/comics_per_characters/paginated?sort_column=name)

[Mongo-Express](http://localhost:8081)

<br>

### Local development
If you want to make some changes in this repo while following the same environment tooling.
```
poetry config virtualenvs.in-project true
poetry install && poetry shell
pre-commit install
```

To change the code of the core containers, you need to `cd` to the related directory and `poetry update`
to install the `dev` dependencies.
