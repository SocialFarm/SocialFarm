CREDENTIALS = socialfarm:success

all : install_apps test

install_apps : 
	# upload mustache.js - used by various show and lists below  
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.js.mustache mustache.js 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.js.mustache mustache.js 

	# public database 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business views.all.map  business/map_all.js	

	# common (same as info for now)
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.default_css info/common/default_css.html
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.navigation info/common/navigation.html

	# list functions rendering the view in html and its dependencies 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business lists.basic_html business/list_basic_html.js 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.list_basic_html business/list_basic.html 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.list_basic_html_row  business/list_basic_row.html  

	# show functions for rendering resource (business json) to html by id
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.show_basic_html business/show_basic.html  
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business shows.basic_html business/show_basic_html.js

	# business template database - is replicated into new businesses in order to inherit apps
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/valid validate_doc_update validate_docs.js

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/scheduler views.offer_tasks.map scheduler/offer_tasks/map.js
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/scheduler views.offer_tasks.reduce scheduler/offer_tasks/reduce.js
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/scheduler views.pending_jobs_tasks.map scheduler/pending_jobs_tasks/map.js
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/scheduler views.pending_jobs_tasks.reduce scheduler/pending_jobs_tasks/reduce.js

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info views.get_start_action.map info/get_start_action/map.js 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info views.all_members.map info/members/map_all.js
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info views.all_actions.map info/actions/map_all.js 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info views.all_jobs.map info/jobs/map_all.js 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info views.all_tasks.map info/tasks/map_all.js

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info lists.members_basic_html info/members/list_basic_html.js
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.members.list_basic_html info/members/list_basic.html 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.members.list_basic_html_row info/members/list_basic_row.html

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info lists.actions_basic_html info/actions/list_basic_html.js
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.actions.list_basic_html info/actions/list_basic.html 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.actions.list_basic_html_row info/actions/list_basic_row.html

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info lists.jobs_basic_html info/jobs/list_basic_html.js
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.jobs.list_basic_html info/jobs/list_basic.html 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.jobs.list_basic_html_row info/jobs/list_basic_row.html

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info lists.tasks_basic_html info/tasks/list_basic_html.js
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.tasks.list_basic_html info/tasks/list_basic.html 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.tasks.list_basic_html_row info/tasks/list_basic_row.html

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.members.show_basic_html info/members/show_basic.html  
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info shows.member_basic_html info/members/show_basic_html.js

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.actions.show_basic_html info/actions/show_basic.html  
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info shows.action_basic_html info/actions/show_basic_html.js

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.jobs.show_basic_html info/jobs/show_basic.html  
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info shows.job_basic_html info/jobs/show_basic_html.js

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.tasks.show_basic_html info/tasks/show_basic.html  
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info shows.task_basic_html info/tasks/show_basic_html.js

	#common
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.default_css info/common/default_css.html 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.navigation info/common/navigation.html  

	#facebook 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info facebook.html.api info/facebook/api.html 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info facebook.html.canvas info/facebook/canvas.html  
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info lists.facebook_canvas info/facebook/canvas.js


clean: 
	./delete_database.py -l $(CREDENTIALS) testbus
	./delete_database.py -l $(CREDENTIALS) testbus2
	./delete_database.py -l $(CREDENTIALS) socialfarm_business_template
	./delete_database.py -l $(CREDENTIALS) socialfarm

test: 
	# create test businesses
	./SocialFarmHelper.py socialfarm success
