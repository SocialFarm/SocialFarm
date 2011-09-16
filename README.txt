Setting up socialfarm.org and http://apps.facebook.com/social_farm/

#########################

There are 2 parts to socialfarm.org:

1. SocialFarm Server 
   This python web server is available at socialfarm/server/server.py.  
   The purpose of this server is to expose a RESTful socialfarm api to the 
   external world.  The server therefore primarily translates the incoming 
   RESTful requests into couchdb calls. For supporting advanced functionality, 
   the server may also implement python code making multiple 
   couchdb and/or external calls. 

   [todo] security 

2. Couchdb  
   This is a localhost instance of couchdb storing underlying socialfarm data. 
   This couchdb is expected to be available only on the localhost as security 
   is offloaded to social farm server. 

   Scalability considerations may require that the local couchdb be replaced by 
   a proxy that routes requests to a set of couchdb instances. 


Manual Operation 
---------------- 

If you wish to use your own (local) version of CouchDB connect to ec2 
machine with remote port forwarding as follows:
    ssh <username>@ec2-50-19-153-41.compute-1.amazonaws.com -R 5984:127.0.0.1:5984;

If you wish to use the instance of couchdb on the ec2 machine, simply remote in 
without any port forwarding.
    ssh <username>@ec2-50-19-153-41.compute-1.amazonaws.com

Once logged in, navigate to the server directory and start the server:
    sudo su;
    cd ~/socialfarm/server;
    python server.py;

You should see this:
    [root@ip-10-203-66-83 server]# python server.py 
    started httpserver at :80

If you would like to start the server on a different port, or with a differnt CouchDB, 
see python server -help

At this point, visit: http://socialfarm.org to confirm the webserver is running.


Automatic Operation i.e. Service Setup
--------------------------------------
The current automatic setup for socialfarm uses daemontools programs to run social 
farm server and couchdb as services. See http://cr.yp.to/daemontools.html for 
details.  

Note on daemontools build.  The downloadble source does not build on amazon ec2 amis.  
The way to solve it is to include an include flas to include errno.h in 
the .cc compilation file. 

The daemontools program requires one to create a directory for each service within the 
/service directory.  Create one such directory for social farm server and one for 
couch db.  The required directory structure is saved in socialfarm/service  
You may need to edit the run files available within this directory structure to point
to the correct couchdb and social farm server directories 



Development and Debugging Reminders:
-----------------------------------

If you are editing documents which are stored in CouchDB you must remake the db to 
view changes. port forwarding is handy here, as you can make local edits and then 
simply remake the db to see the changes in production.

If you are editing anything in the server directory you must make sure the ec2 machine 
is up to date, I usually commit local changes and then 'svn up' on the ec2 machine, 
but this is not the only (or best) way.

[todo ?] : we can possibly write a small rsync script to sycnhronize the server code with 
local uncomitted changes.  that would take care of this uncessary commit issue.  see 
man rsync. 






