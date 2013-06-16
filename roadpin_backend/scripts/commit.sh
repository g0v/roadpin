#!/bin/bash

if [ "${BASH_ARGC}" != "3" ]
then
  echo "usage: commit.sh [message] [host] [branch]"
  exit 0
fi

message=${BASH_ARGV[2]}
host=${BASH_ARGV[1]}
branch=${BASH_ARGV[0]}

git add .; git commit -m "${message}"; git push; ./scripts/deploy_update.sh ${branch} 1 ${host}
