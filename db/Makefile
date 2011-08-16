CREDENTIALS = socialfarm:success

all : clean install_apps test

install_apps : 
	# upload mustache.js - used by various show and lists below  
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.js.mustache common/js/mustache.js 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.js.mustache common/js/mustache.js 

	# public database 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business views.all_businesses.map  business/map_all.js	

	# common (same as info for now)
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.default_css common/default_css.html
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.default_css common/default_css.html 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.default_js common/default_js.html
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info common.html.default_js common/default_js.html 

	# list functions rendering the view in html and its dependencies 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business lists.basic_html business/list_basic_html.js 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.list_basic_html business/list_basic.html 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.list_basic_html_row  business/list_basic_row.html  

	# show functions for rendering resource (business json) to html by id
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.html.show_basic_html business/show_basic.html  
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business shows.basic_html business/show_basic_html.js
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business common.js.socialfarm common/js/socialfarm.js


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

	#facebook 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business facebook.html.navigation facebook/navigation.html 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business facebook.html.canvas facebook/canvas.html
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business facebook.html.join_business_html facebook/join_business.html 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business facebook.html.facebook_footer facebook/facebook_footer.html
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business facebook.html.FBOnLoad facebook/FBOnLoad.html
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business lists.facebook_canvas facebook/canvas.js
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business shows.join_business facebook/join_business.js

	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info facebook.html.facebook_footer facebook/facebook_footer.html 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info facebook.html.navigation facebook/navigation.html 
	./update_field.py -l $(CREDENTIALS) socialfarm_business_template _design/info facebook.html.facebook_footer facebook/facebook_footer.html

	./update_field.py -l $(CREDENTIALS) socialfarm _design/business views.my_businesses.map  facebook/map_my_businesses.js
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business facebook.html.my_businesses_html facebook/my_businesses.html 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business shows.my_businesses facebook/my_businesses.js

	./update_field.py -l $(CREDENTIALS) socialfarm _design/business views.my_tasks.map  facebook/map_my_businesses.js
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business facebook.html.my_tasks_html facebook/my_tasks.html 
	./update_field.py -l $(CREDENTIALS) socialfarm _design/business shows.my_tasks facebook/my_tasks.js







clean: 
	./delete_database.py -l $(CREDENTIALS) testbus
	./delete_database.py -l $(CREDENTIALS) testbus2
	./delete_database.py -l $(CREDENTIALS) socialfarm_business_template
	./delete_database.py -l $(CREDENTIALS) socialfarm


test: 
	# create test businesses
	./SocialFarmHelper.py socialfarm success
