#!/bin/bash

if [ "${BASH_ARGC}" != 3 ]
then
  echo "usage: deploy_install.sh [branch] [n_proc] [host]"
  exit 0
fi

branch=${BASH_ARGV[2]}
n_proc=${BASH_ARGV[1]}
host=${BASH_ARGV[0]}

echo "deploy_install.sh branch: ${branch} n_proc: ${n_proc} host: ${host}"

echo "to update"
fab -H ${host} -f deploy install.update:branch=${branch},n_proc=${n_proc}
