#!/bin/bash

if [ "${BASH_ARGC}" != "3" ]
then
  echo "usage: backend_server.sh [ini_filename] [log_filename] [port]"
  exit 0
fi

ini_filename=${BASH_ARGV[2]}
log_filename=${BASH_ARGV[1]}
port=${BASH_ARGV[0]}

filename_first_letter=`echo ${ini_filename}|head -c 1`
echo "ini_filename: ${ini_filename} filename_first_letter: ${filename_first_letter}"
if [ "${filename_first_letter}" != "/" ]
then
  ini_filename="`pwd`/${ini_filename}"
fi

filename_first_letter=`echo ${log_filename}|head -c 1`
echo "log_filename: ${log_filename} filename_first_letter: ${filename_first_letter}"
if [ "${filename_first_letter}" != "/" ]
then
  log_filename="`pwd`/${log_filename}"
fi

echo "ini_filename: ${ini_filename} log_filename: ${log_filename}"

cd roadpin_backend
. __/bin/activate
python -m app.main -i "${ini_filename}" -l "${log_filename}" -p "${port}"
cd ..
