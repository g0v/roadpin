
Project overview
================

     The goal of this project is to quickly test against Smaato OpenRTB 2.0 to see what is the expected data format and concurrency. 

Implementation Plan
===================
     1. We will use bottle and gevent as server. 
     2. The point here is quickly check out the target data format. We will migrate to Java in the future, given that we have better understanding 
        on what we are facing.


How to use this implementation
==============================
	1. The test case is defined in test.py. Please use nosetests to test. 
	2. The main program is main.py. It runs at localhost:80
	3. The RTB endpoint is at http://[public ip]/req/[rtb provider Id]. POST only
	   You may want to give each SSP different endpoint
	4. THe callback endpoint is located at http://[public ip]/win. GET only. 
	5. All request logs go to myapp.log. The main.py appends logs to the file for every launch.

Project File Structure
======================
    1. main.py : main program & all HTTP endpoint routes.
    2. rtbbidder.py : RTB bidder logics. 
    3. openrtb.py : OpenRTB data strucutres
    4. campaigns.py : Our Ad Campaign Definitions
    5. test.py : nosetest test cases


Smaato auction simulation request
=================================

	To pass the simulation, we need to provide following results:

	1. Total number of bids
	2. Total number of no bids
	3. Won auctions
	4. Total bid price
	5. Total won price
