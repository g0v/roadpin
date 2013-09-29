#!/bin/bash

source /etc/profile.d/rvm.sh

rm -rf _public
node_modules/brunch/bin/brunch watch --server -P
