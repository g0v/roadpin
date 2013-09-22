#!/bin/bash

lsc -cb test/karma-e2e.conf.ls
mv test/karma-e2e.conf test/karma-e2e.conf.js
node_modules/karma/bin/karma start test/karma-e2e.conf.js

