#!/bin/bash

if [ "${BASH_ARGC}" != "4" ]
then
  echo "usage: deploy_update.sh [ssh_key] [branch] [n_proc] [host]"
  exit 0
fi

ssh_key=${BASH_ARGV[3]}
branch=${BASH_ARGV[2]}
n_proc=${BASH_ARGV[1]}
host=${BASH_ARGV[0]}

echo "deploy_update.sh branch: ${branch} n_proc: ${n_proc} host: ${host}"

echo "to update"
fab -P -i ${ssh_key} -H ${host} -f deploy install.update:branch=${branch},n_proc=${n_proc}
