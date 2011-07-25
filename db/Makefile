


all : install_apps test 

install_apps : 
	# upload mustache.js - used by various show and lists below  
	./update_field.py -l socialfarm:success socialfarm _design/business common.js.mustache mustache.js 
	# public database 
	./update_field.py -l socialfarm:success socialfarm _design/business views.list.map  business/list/map.js	
	# list function rendering the view in html and its dependencies 
	./update_field.py -l socialfarm:success socialfarm _design/business lists.facebook_list_businesses business/list/facebook_list_businesses.js
	./update_field.py -l socialfarm:success socialfarm _design/business common.html.facebook_list_businesses business/list/facebook_list_businesses.html 
	./update_field.py -l socialfarm:success socialfarm _design/business common.html.facebook_list_businesses_row business/list/facebook_list_businesses_row.html 
	# facebook show business
	./update_field.py -l socialfarm:success socialfarm _design/business common.html.facebook business/facebook_show.html 
	./update_field.py -l socialfarm:success socialfarm _design/business shows.facebook_show  business/facebook_show.js 
	# business template database - is replicated into new businesses in order to inherit apps
	./update_field.py -l socialfarm:success socialfarm_business_template _design/valid validate_doc_update validate_docs.js
	./update_field.py -l socialfarm:success socialfarm_business_template _design/scheduler views.offer_tasks.map scheduler/offer_tasks/map.js
	./update_field.py -l socialfarm:success socialfarm_business_template _design/scheduler views.offer_tasks.reduce scheduler/offer_tasks/reduce.js
	./update_field.py -l socialfarm:success socialfarm_business_template _design/scheduler views.pending_jobs_tasks.map scheduler/pending_jobs_tasks/map.js
	./update_field.py -l socialfarm:success socialfarm_business_template _design/scheduler views.pending_jobs_tasks.reduce scheduler/pending_jobs_tasks/reduce.js
	./update_field.py -l socialfarm:success socialfarm_business_template _design/info views.get_start_action.map info/get_start_action/map.js 
	./update_field.py -l socialfarm:success socialfarm_business_template _design/info views.list_actions.map info/list_actions/map.js 
	./update_field.py -l socialfarm:success socialfarm_business_template _design/info views.list_members.map info/list_members/map.js



test: 
	# create test businesses
	./SocialFarmHelper.py socialfarm success
