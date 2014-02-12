#!/bin/bash

if [ "${BASH_ARGC}" != "3" ]
then
  echo "usage: backend_server.sh [ini_filename] [log_filename] [port]"
  exit 0
fi

ini_filename=${BASH_ARGV[2]}
log_dir=${BASH_ARGV[1]}
port=${BASH_ARGV[0]}

cd roadpin_backend
. __/bin/activate
python -m app.main -i ${ini_filename} -l ${log_filename} -p ${port}
cd ..
