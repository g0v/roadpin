# -*- coding: utf-8 -*-

import logging; 
import time
from urllib2 import urlopen
from fabric.api import *
from fabric.colors import *
from deploy import util
import re

PROJECT_NAME = "roadpin"

@task    
def install_stage1(branch = 'master', n_proc = '4'):
    target_host = env.host_string
    _git_clone(target_host, branch)
    _install_production_ini(target_host, n_proc, 'production.ini')
    _set_virtualenv(target_host)
    _install_packages(target_host)
    _install_log_dir(target_host)


@task    
def install_staging(branch = 'master', n_proc = '4'):
    target_host = env.host_string
    _git_clone(target_host, branch)
    _install_production_ini(target_host, n_proc)
    _set_virtualenv(target_host)
    _install_packages(target_host)
    _install_log_dir(target_host)


@task
def update(branch = 'master', n_proc = '4'):
    target_host = env.host_string
    _git_pull(target_host, branch)
    _install_packages(target_host)
    _install_log_dir(target_host)


def _git_clone(target_host, branch = 'master'):    
    with cd("/srv"):
        try:
            run("git clone -b " + branch + " https://github.com/ronnywang/roadpin")
        except:
            print(red("[ERROR] unable to git clone"))


def _git_pull(target_host, branch = 'master'):    
    with cd("/srv/" + PROJECT_NAME):
        try:
            run("git reset --hard")
            run("git pull")
            run("git checkout " + branch)
            run("git pull")
        except:
            print(red("[ERROR] unable to git pull"))


def _set_virtualenv(target_host, virtualenv_dir='__'):
    with cd("/srv/roadpin/roadpin_backend"):
        run("./scripts/init_pcreate.sh " + virtualenv_dir)


def _install_packages(target_host, virtualenv_dir='__'):
    with cd("/srv/roadpin/roadpin_backend"), prefix("source " + virtualenv_dir + "/bin/activate"):
        run("pwd")
        run("which python")
        run("pip install -r requirements.txt")


def _install_production_ini(target_host, n_proc, ini_filename='staging.ini', virtualenv_dir='__'):
    target_host_no_dot = re.sub(ur'\.', '_', target_host, re.M | re.U)
    print(green('target_host:' + repr(target_host) + ' taregt_host_no_dot:' + repr(target_host_no_dot)))
    with cd("/srv/roadpin/roadpin_backend"):
        run("cp " + ini_filename + ' /etc/roadpin/production.ini')


def _install_log_dir(target_host):
    try:
        run("mkdir -p /var/log/roadpin")
    except:
        print(red("[ERROR] unable to mkdir -p /var/log/roadpin"))
