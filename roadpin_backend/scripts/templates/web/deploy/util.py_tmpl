from fabric.api import *
from fabric.colors import *

def is_set(cmd, prompt):
    is_set = True
    result = None
    try: 
        result = sudo(cmd)
        if result == '':
            is_set = False
    except:
        is_set = False
    print(yellow(prompt + "::grep:" + str(result)))
    return is_set

def google_doc_mark(target_host, params):
    pass
