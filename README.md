# biggie
<br>

Toolkit based on Spark, Celery, FastAPI and Mongo.
Currently set up with an API harvester fine-tuned for the [Marvel API](https://developer.marvel.com).
<br>


#### Installation
You should use the `main` branch, other branches being used for development purpose.

Update the `compose` files for the `api_test / api_prod / celery` services where you might want to change the `volumes` to mount your data/logs within.

Then you're left with creating the `.env` environment file, most important with your Marvel API keys.

*NB: For all these required files, you'll find `xxxxxx.example` sample files ready to adapt.*

<br>

#### Run
Only the core containers
```
docker-compose -f docker-compose.core.yml up
```

\+ monitoring containers
```
docker-compose -f docker-compose.core.yml -f docker-compose.monitoring.yml up
```

\+ full app (including test container)

When started, this command will:
- download all the data from the Marvel characters API
- load it into Mongo
- start a FastAPI application for all the required data/reporting endpoints
```
docker-compose -f docker-compose.core.yml -f docker-compose.monitoring.yml -f docker-compose.app.yml up
```
<br>

#### Nginx deployment
You have to create the required files and change the `volumes` path accordingly in the `compose` files.
The `nginx` configuration files are:
- `conf/nginx/certificate.json`
- `conf/nginx/app_docker.conf`
- `conf/nginx/monitor_docker.conf`

```
docker-compose -f docker-compose.core.yml -f docker-compose.app.yml -f docker-compose.monitoring.yml --profile live_prod up
```
<br>



#### Local URLs

[API docs](http://localhost:8000/docs)

API - Results full list
- [sorted by comics number](http://localhost:8000/api/comics_per_characters?sort_column=comics_available)
- [sorted by name](http://localhost:8000/api/comics_per_characters?sort_column=name)

API - [WIP] Paginated results
- [sorted by comics number](http://localhost:8000/api/comics_per_characters/paginated?sort_column=comics_available)
- [sorted by name](http://localhost:8000/api/comics_per_characters/paginated?sort_column=name)

[Mongo-Express](http://localhost:8081)

[Flower](http://localhost:49555)

<br>

#### Development
If you want to make some changes in this repo while following the same environment tooling.
```
poetry config virtualenvs.in-project true
poetry install && poetry shell
pre-commit install
```

<br>

#### Docker considerations
Docker is great but sometimes tricky ... when changes are made, don't forget to:
- Use the `--build` flag.
- Cleanse the database properly by using the `prune` and `rm` tools to purge volumes and containers.

<br>
