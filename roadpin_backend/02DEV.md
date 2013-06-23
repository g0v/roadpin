REQUIREMENT:
==========
1. must git-clone as scripts

To init pcreate:
==========
scripts/init_pcreate.sh

To create egg info (for pcreate and many other things)
==========
scripts/egg_info.sh

To create a dev module dummy3.dummy4.dummy5
==========
scripts/dev.sh dummy3.dummy4.dummy5

To run autotest (re-test for every file change):
==========
scripts/autotest.sh

To run test:
==========
scripts/test.sh

or

nosetests tests

To run test on single file/subdir:
==========
scripts/test_single.sh [filename]

or

nosetests [filename]
