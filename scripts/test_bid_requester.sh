#!/bin/bash
ssh root@192.168.168.191 "cd bid-requester; ./loadtest_with_file.sh 1 14 0.1 'http://192.168.168.134:8000/ortb/mopub' 0.001 /root/bid_requester/data/athena_head_20"
