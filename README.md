This LinMin project is still incomplete. The preoject tries to collect system stat and provides you on web UI.

Install Systat

sudo apt-get install sysstat

Edit /etc/sysstat.conf and set true 

start service

sudo service sysstat restart

Please run sudo python api/mined_data.py 

and run python -m SimpleHTTPServer 

to see results.

 
