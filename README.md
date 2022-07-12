# biggie
<br>
Biggie is a tool to quickly get data from (external) APIs into a Mongo database,
and have it exposed/searchable via a dedicated new API.

It is a Docker setup with 3 main containers based on Spark, FastAPI and Mongo.
Additional containers can be setup for Mongo Express and Nginx.

Currently set up with an API harvester fine-tuned for the [Marvel API](https://developer.marvel.com).

<br>


### Installation

#### Environment
You have to create the `.env` environment file, most important including your Marvel API keys.
If you plan to use the same Github-actions CI file,
you need to create the same secrets as in your `.env` environment file.

**NB**:
- For all these required files, you'll find the `.env.example` file ready to adapt.
- The `VOLUME_MOUNT` **Github-action secret** does NOT take the usual `./` for a relative path from the host
e.g. `./some/path:/some/new/path` becomes `some/path:/some/new/path`.

<br>

#### Build
The `docker-compose.main` file is structured to make the `test` containers build the image
used by the `prod` image. Hence the need to run one of the following commands on the very first run:
```
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml up pyspark_test harvester_test api_test
OR
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml --profile test up
```

<br>

**NB**: you can also bypass this `build` step by directly pulling the images ...
```
docker pull ghcr.io/pierrz/biggie_pyspark_img:latest
docker pull ghcr.io/pierrz/biggie_harvester_img:latest
docker pull ghcr.io/pierrz/biggie_api_img:latest
```

... and replace the image reference for each container accordingly
(by removing the `build` section),
such as the following for the API containers:

```image: "ghcr.io/pierrz/biggie_api_img:latest"```

<br>

### Run
#### Data acquisition and load
```
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml up pyspark_prod
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
# only pyspark_prod api_prod containers visible in the terminal
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml --profile monitoring up pyspark_prod api_prod
```
OR
```
# all containers visible in the terminal
docker-compose -f docker-compose.main.yml -f docker-compose.mongo.yml --profile prod --profile monitoring up
```

<br>

### Nginx deployment (API container only)
In this configuration, you need to have the necessary sub-domains setup on your domain provider side.
You also need:
- Nginx installed on the host machine
- a certificate generated by `certbot` without any changes to nginx configuration (see [documentation](https://certbot.eff.org/instructions))
    ```
    sudo certbot certonly --nginx    # example command for ubuntu 20
    ```
<br>

Then create the required files and change the `volumes` path accordingly in the `compose` files.
The `nginx` configuration files are:

`conf/nginx/certificate.json`
`conf/nginx/app_docker.conf`
`conf/nginx/monitor_docker.conf`
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
If you want to make some changes in this repo while following the same environment tooling,
you can run the following command from the root directory:
```
poetry config virtualenvs.in-project true
poetry install && poetry shell
pre-commit install
```

To change the code of the core containers, you need to `cd` to the related directory
and either:
- run `poetry update` to simply install the required dependencies
- run the previous command to create a dedicated virtualenv
