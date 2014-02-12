#!/bin/bash

cd roadpin-frontend

while [ 1 -eq 1 ]
do
  node_modules/brunch/bin/brunch watch -P --server
  sleep 1
done

cd ..
