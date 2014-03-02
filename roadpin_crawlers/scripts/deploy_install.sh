#!/bin/bash

if [ "${BASH_ARGC}" != "4" ]
then
  echo "usage: deploy_install.sh [ssh_key] [branch] [n_proc] [host]"
  exit 0
fi

ssh_key=${BASH_ARGV[3]}
branch=${BASH_ARGV[2]}
n_proc=${BASH_ARGV[1]}
host=${BASH_ARGV[0]}

echo "deploy_install.sh branch: ${branch} n_proc: ${n_proc} host: ${host}"

echo "to install_stage1"
fab -i ${ssh_key} -H ${host} -f deploy install.install_stage1:branch=${branch},n_proc=${n_proc}
