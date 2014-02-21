#!/bin/bash

while [ 1 -eq 1 ]
do
  rm -rf _public
  if [ ! -e "production.ls" ]
  then
    ln -s production.ls_tmpl production.ls
  fi
  node_modules/brunch/bin/brunch watch --server
  sleep 1
done
