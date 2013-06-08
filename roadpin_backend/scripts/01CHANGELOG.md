

Testing progress
================

4422ced has passed smaato compliance tests for text ad, image ad and richmedia ad.


56ca2d201ab1276f0a5da14bebd4a670f53232b3 update to newer way of doing things:


    1. use supervisord to handle everything. 

       supervisor conf is saved in deploy/supervisor

       virtualenv setup script is env_run.sh

       right now we assume rtbbidder is saved at /srv/rtbbidder

       also, we save logs at  /srv/rtbbidder/log 

    2. use tornado and do graceful stop.

        Note: each main.py starts one process and bind to one port. we use Load Balander to distribute loads among them.

        reference : http://www.keakon.net/2012/12/17/%E7%94%9F%E4%BA%A7%E7%8E%AF%E5%A2%83%E4%B8%8B%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E5%9C%B0%E9%87%8D%E5%90%AFTornado

    3. main.py now takes an integer as port

    Environment setup:

       we use linode NodeBalancer to distribute loads among bidders. Each bidder runs at its own port.  
       we expect local redis has a domain socket at /tmp/redis.sock with permission 777

    Usage

       to use supervisor to restart:

       supervisorctl restart rtbbidder:*

