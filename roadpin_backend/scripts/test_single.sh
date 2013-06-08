#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: test_single.sh [filename]"
  exit 0
fi

filename=${BASH_ARGV[0]}

nosetests ${filename}
