#!/bin/bash

cd roadpin_backend
virtualenv __
. __/bin/activate
pip install -r requirements.txt
cd ..
deactivate

cd roadpin-frontend
./scripts/init.sh
cd ..


