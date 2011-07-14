### Here are some notes for developing the social_farm pyramid application
### Orie Steele

Install Python
    $ sudo apt-get install python python-setuptools

Install virtualenv
    $ sudo easy_install virtualenv

Setup virtualenv in directory pyramidDevEnv
    $ virtualenv --no-site-packages social_farm_env

Activate virtualenv
    $ cd social_farm_env
    $ source bin/activate

Install pyramid
    $ easy_install pyramid

Creating a pyramid app
    http://docs.pylonsproject.org/projects/pyramid/dev/narr/project.html
        $ bin/paster create -t pyramid_starter
        $ easy_install pyramid_handlers
        $ easy_install simplejson
    http://docs.pylonsproject.org/projects/pyramid_cookbook/dev/couchdb.html
        $ easy_install couchdb

Configuring ModWSGI

before the virtual host block for you app make sure to specify, 
the python path using the appropriate virtual env:
 
WSGIPythonPath /usr/local/pyramid/social_farm_env/lib/python2.6/site-packages

see httpd-vhost.conf for virtual host configuration
