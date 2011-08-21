Setting up socialfarm.org
#########################

There are 2 parts to socialfarm.org, the python web server (socialfarm/server/server.py) and a localhost instance of couchdb.

If you wish to use your own (local) version of CouchDB connect to ec2 machine with remote port forwarding as follows:


    ssh <username>@ec2-50-19-153-41.compute-1.amazonaws.com -R 5984:127.0.0.1:5984;

If you wish to use the instance of couchdb on the ec2 machine, simply remote in without any port forwarding.

    ssh <username>@ec2-50-19-153-41.compute-1.amazonaws.com

Once logged in, navigate to the server directory and start the server:

    sudo su;
    cd ~/socialfarm/server;
    python server.py;

You should see this:

    [root@ip-10-203-66-83 server]# python server.py 
    started httpserver at :80

If you would like to start the server on a different port, or with a differnt CouchDB, see python server -help

At this point, visit: http://socialfarm.org to confirm the webserver is running.

Development and Debugging Reminders:

    If you are editing documents which are stored in CouchDB you must remake the db to view changes. port forwarding is handy here, as you can make local edits and than simply remake the db to see the changes in production.
    If you are editing anything in the server directory you must make sure the ec2 machine is up to date, I usually commit local changes and then 'svn up' on the ec2 machine, but this is not the only (or best) way.






