#!/bin/bash
set -e

echo "MongoDB initialization from Compose ..."

mongosh <<EOF
db.auth('$MONGO_INITDB_ROOT_USERNAME', '$MONGO_INITDB_ROOT_PASSWORD')

db = db.getSiblingDB('$DB_NAME')

db.createUser({
  user: '$MONGO_USERNAME',
  pwd: '$MONGO_PASSWORD',
  roles: [
    {
      role: 'readWrite',
      db: '$DB_NAME',
    },
  ],
})
EOF

echo "MongoDB initialized."
