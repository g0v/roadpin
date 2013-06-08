#!/bin/bash

if [ "${BASH_ARGC}" != 1 ]
then
  echo "usage: run_web_dev.sh [port]"
  exit 0
fi

port=${BASH_ARGV[0]}

python -m app.main ${port} development.ini
