#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: frontend_server.sh [port]"
  exit 0
fi

port=${BASH_ARGV[0]}

cd roadpin-frontend

if [ ! -e "ini/production.ls" ]
then
  mkdir -p ini
  cp production.ls_tmpl ini/production.ls
fi

while [ 1 -eq 1 ]
do
  node_modules/brunch/bin/brunch watch -P --server -p ${port}
  sleep 1
done

cd ..
