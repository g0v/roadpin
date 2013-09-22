#!/bin/bash

while [ 1 -eq 1 ]
do
  rm -rf _public
  node_modules/brunch/bin/brunch watch --server
  sleep 1
done
