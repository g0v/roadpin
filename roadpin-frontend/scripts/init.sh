#!/bin/bash

rm -rf node_modules
npm install

rm -rf bower_components
bower install

#jade 
echo "[INFO] to jade"
filename=node_modules/jade-brunch/vendor/runtime.js
sed 's/^jade = /window.jade = /g' ${filename} > ${filename}.tmp
mv ${filename}.tmp ${filename}

#livescript-prelude
#echo "[INFO] to livescript-prelude"
#filename=node_modules/LiveScript-brunch/vendor/prelude-browser-0.6.0.js
#sed 's/^  exports = {};/  var exports = {};/g' ${filename} > ${filename}.tmp
#mv ${filename}.tmp ${filename}
