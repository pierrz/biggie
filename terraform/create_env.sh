#!/bin/sh

echo "# Docker routing" >> .env
echo "DOCKER_SUBNET_BASE=${var.docker_subnet_base}" >> .env
echo "COMPOSE_PREFIX=${var.compose_prefix}" >> .env
echo "SPARK_PORTS_RANGE=${var.spark_ports_range}" >> .env
echo "RABBITMQ_PORT=${var.rabbitmq_port}" >> .env
echo "DATA_DIR=${var.data_dir}" >> .env
echo "LOGS_DIR=${var.logs_dir}" >> .env
echo "CELERY_BROKER_URL=${var.celery_broker_url}" >> .env
echo "CELERY_RESULT_BACKEND=${var.celery_result_backend}" >> .env
echo "" >> .env
echo "# DBs" >> .env
echo "DB_NAME=${var.db_name}" >> .env
echo "# PostgresSQL" >> .env
echo "POSTGRES_DB=${var.postgres_db}" >> .env
echo "POSTGRES_USER=${var.postgres_user}" >> .env
echo "POSTGRES_PASSWORD=${var.postgres_password}" >> .env
echo "POSTGRES_APP_USER=${var.postgres_app_user}" >> .env
echo "POSTGRES_APP_PASSWORD=${var.postgres_app_password}" >> .env
echo "POSTGRES_PORT=${var.postgres_port}" >> .env
echo "# MongoDB" >> .env
echo "MONGO_INITDB_ROOT_USERNAME=${var.mongo_initdb_root_username}" >> .env
echo "MONGO_INITDB_ROOT_PASSWORD=${var.mongo_initdb_root_password}" >> .env
echo "MONGO_USERNAME=${var.mongo_username}" >> .env
echo "MONGO_PASSWORD=${var.mongo_password}" >> .env
echo "MONGO_PORT=${var.mongo_port}" >> .env
echo "" >> .env
echo "# SERVICES" >> .env
echo "# Orchestrator" >> .env
echo "TOKEN_GITHUB_API=${var.token_github_api}" >> .env
echo "# API" >> .env
echo "API_PORT=${var.api_port}" >> .env
echo "# Jupyter" >> .env
echo "JUPYTER_PASSWORD=${var.jupyter_password}" >> .env
echo "JUPYTER_PORT=${var.jupyter_port}" >> .env
echo "" >> .env
echo "# Monitoring" >> .env
echo "# Flower" >> .env
echo "FLOWER_PORT=${var.flower_port}" >> .env
echo "# DBeaver" >> .env
echo "DBEAVER_PORT=${var.dbeaver_port}" >> .env
echo "# Mongo-Express" >> .env
echo "ME_CONFIG_MONGODB_ADMINUSERNAME=${var.me_config_mongodb_adminusername}" >> .env
echo "ME_CONFIG_MONGODB_ADMINPASSWORD=${var.me_config_mongodb_adminpassword}" >> .env
echo "ME_CONFIG_BASICAUTH_USERNAME=${var.me_config_basicauth_username}" >> .env
echo "ME_CONFIG_BASICAUTH_PASSWORD=${var.me_config_basicauth_password}" >> .env
echo "ME_CONFIG_PORT=${var.me_config_port}" >> .env
