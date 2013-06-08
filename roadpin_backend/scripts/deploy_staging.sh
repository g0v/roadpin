#!/bin/bash

if [ "${BASH_ARGC}" != 3 ]
then
  echo "usage: deploy_staging.sh [branch] [n_proc] [host]"
  exit 0
fi

branch=${BASH_ARGV[2]}
n_proc=${BASH_ARGV[1]}
host=${BASH_ARGV[0]}

echo "deploy_staging.sh branch: ${branch} n_proc: ${n_proc} host: ${host}"

echo "to install_staging"
fab -H ${host} -f deploy install.install_staging:branch=${branch},n_proc=${n_proc}
echo "to install_postinstall"
fab -H ${host} -f deploy install.install_postinstall:n_proc=${n_proc}
