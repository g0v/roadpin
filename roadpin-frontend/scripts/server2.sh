#!/bin/bash

source /etc/profile.d/rvm.sh

rm -rf _public
exec $@
