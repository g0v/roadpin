#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: scripts/dev.sh ${BASH_ARGV[0]}"
  exit 0
fi

module=${BASH_ARGV[0]}

module_without_leading_app=`echo "${module}"|sed 's/^app\.//g'`
module_with_slash=`echo "${module_without_leading_app}"|sed 's/\./\//g'`

echo "[INFO] to create module with class: ${module_with_slash}"
pcreate -s simple ${module_with_slash} -d .

pre_pkg=""
arr=$(echo ${module}|tr "." "\n")
for each_pkg in ${arr[@]}
do
  echo "each_pkg: ${each_pkg}"
  if [ "${pre_pkg}" != "" ]
  then
    echo "[INFO] to create pkg: ${pre_pkg}"
    pcreate -s pkg ${pre_pkg} -d .
    pre_pkg="${pre_pkg}/"
  fi
  pre_pkg="${pre_pkg}${each_pkg}"
done
