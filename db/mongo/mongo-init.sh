#!/bin/bash
set -e

echo "MongoDB initialization from Compose ..."

mongosh admin -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" <<EOF
  use $DB_NAME
  db.createUser({
    user: "$MONGO_USERNAME",
    pwd: "$MONGO_PASSWORD",
    roles: [{ role: "readWrite", db: "$DB_NAME" }]
  })
EOF

echo "MongoDB initialized."
