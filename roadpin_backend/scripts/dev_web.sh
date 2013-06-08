#!/bin/bash

current_dir=`pwd`
module=`basename ${current_dir}`

module_without_leading_app=`echo "${module}"|sed 's/^app\.//g'`
module_with_slash=`echo "${module_without_leading_app}"|sed 's/\./\//g'`

echo "[INFO] to create module: ${module_with_slash}"
pcreate -s web ${module_with_slash} -d .
