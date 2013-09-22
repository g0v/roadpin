#!/bin/bash

lsc -cb test/karma-unit.conf.ls
mv test/karma-unit.conf test/karma-unit.conf.js
node_modules/karma/bin/karma start test/karma-unit.conf.js
