#!/bin/bash
export PGPASSWORD=secret
psql -h postgres -U postgres -c "CREATE ROLE frespo LOGIN  password 'frespo' NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;"
createdb -h postgres -U postgres -O frespo frespo