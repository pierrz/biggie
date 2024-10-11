#!/bin/bash
set -e

echo "MongoDB initialization from Compose ..."

mongosh admin -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" <<EOF

  // Client user
  use $DB_NAME
  db.createUser({
    user: "$MONGO_USERNAME",
    pwd: "$MONGO_PASSWORD",
    roles: [{ role: "readWrite", db: "$DB_NAME" }]
  })

  // Mongo Express user
  use admin
  db.createUser({
    user: "$ME_CONFIG_MONGODB_ADMINUSERNAME",
    pwd: "$ME_CONFIG_MONGODB_ADMINPASSWORD",
    roles: [
      { role: "readAnyDatabase", db: "admin" },
      { role: "dbAdminAnyDatabase", db: "admin" },
      { role: "userAdminAnyDatabase", db: "admin" },
      { role: "clusterMonitor", db: "admin" }
    ]
  })

EOF

echo "MongoDB initialized."
