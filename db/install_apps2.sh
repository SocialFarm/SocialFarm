#!/bin/bash

# public database 
./update_field.py -l socialfarm:success socialfarm _design/business views.list.map  business/list/map.js

./update_field.py -l socialfarm:success socialfarm _design/business shows.facebook_show  business/facebook_show.js 

# mustache test 
./update_field.py -l socialfarm:success socialfarm _design/business common.js.mustache business/mustache.js 
./update_field.py -l socialfarm:success socialfarm _design/business common.html.mustache business/mustache_show.html 
./update_field.py -l socialfarm:success socialfarm _design/business shows.mustache_show  business/mustache_show.js


# business template database 
./update_field.py -l socialfarm:success socialfarm_business_template _design/valid validate_doc_update validate_docs.js

./update_field.py -l socialfarm:success socialfarm_business_template _design/scheduler views.offer_tasks.map scheduler/offer_tasks/map.js
./update_field.py -l socialfarm:success socialfarm_business_template _design/scheduler views.offer_tasks.reduce scheduler/offer_tasks/reduce.js


./update_field.py -l socialfarm:success socialfarm_business_template _design/scheduler views.pending_jobs_tasks.map scheduler/pending_jobs_tasks/map.js
./update_field.py -l socialfarm:success socialfarm_business_template _design/scheduler views.pending_jobs_tasks.reduce scheduler/pending_jobs_tasks/reduce.js

./update_field.py -l socialfarm:success socialfarm_business_template _design/info views.get_start_action.map info/get_start_action/map.js 


./update_field.py -l socialfarm:success socialfarm_business_template _design/info views.list_actions.map info/list_actions/map.js 


./update_field.py -l socialfarm:success socialfarm_business_template _design/info views.list_members.map info/list_members/map.js

