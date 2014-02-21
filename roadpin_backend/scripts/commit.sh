#!/bin/bash

if [ "${BASH_ARGC}" != "2" ]
then
  echo "usage: commit.sh [message] [branch]"
  exit 0
fi

message=${BASH_ARGV[1]}
branch=${BASH_ARGV[0]}

git add .; git commit -m "${message}"; git push -u origin ${branch}
