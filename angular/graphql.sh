#!/bin/bash
MYUSER=${1:-postgres}
MYPORT=${2:-5432}
MYHOST=${3:-127.0.0.1}
DATABASE=${4:-caloriestracker}
DEBUG="graphile-build:warn" postgraphile --cors -c postgres://$MYUSER:$PGPASSWORD@$MYHOST:$MYPORT/$DATABASE --enhance-graphiql
