#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  virtualenv_dir="__"
else
  virtualenv_dir="${BASH_ARGV[0]}"
fi  

init_pcreate_current_dir=`pwd`

script_dir="scripts"

echo "virtualenv_dir: ${virtualenv_dir}"

if [ ! -d ${virtualenv_dir} ]
then
  echo "no ${virtualenv_dir}. will create one"
  virtualenv -p `which python` --no-site-packages "${virtualenv_dir}"
fi

cd ${virtualenv_dir}
source bin/activate
the_python_path=`which python`
echo "python: ${the_python_path}"

if [ ! -f "bin/pcreate" ]
then
  git clone https://github.com/chhsiao1981/pyramid.git lib/pcreate

  echo "to lib/pcreate"
  cd lib/pcreate
  pwd

  echo "to checkout pcreate"
  git checkout pcreate

  echo "to setup.py dev"
  python setup.py dev

  echo "to setup.py test"
  python setup.py test
fi

cd ${init_pcreate_current_dir}

echo "current_dir: "
pwd

#requires
pip install sniffer
pip install MacFSEvents #for mac
pip install pywin32     #for windows
pip install pyinotify   #for linux

echo "cp ${script_dir}/setup.py"
cp ${script_dir}/setup.py ./
cp ${script_dir}/*.md ./

echo "remove CHANGES.txt"
rm CHANGES.txt

echo "remove MANIFEST.in"
rm MANIFEST.in

echo "remove README.txt"
rm README.txt
python setup.py egg_info
python setup.py develop
rm -rf scripts/.git
