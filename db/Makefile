cred = socialfarm:success

all : install_apps test

install_apps : 
	# upload mustache.js - used by various show and lists below  
	./update_field.py -l $(cred) socialfarm _design/business common.js.mustache mustache.js 
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.js.mustache mustache.js 

	# public database 
	./update_field.py -l $(cred) socialfarm _design/business views.list_businesses.map  business/list_businesses/map.js	

	# list functions rendering the view in html and its dependencies 
	./update_field.py -l $(cred) socialfarm _design/business lists.business_list business/list_businesses/business_list.js
	./update_field.py -l $(cred) socialfarm _design/business common.html.business_list business/list_businesses/business_list.html 
	./update_field.py -l $(cred) socialfarm _design/business common.html.business_list_row business/list_businesses/business_list_row.html 

	# show functions rendering resource to html by id
	./update_field.py -l $(cred) socialfarm _design/business common.html.business_show business/show_business/business_show.html 
	./update_field.py -l $(cred) socialfarm _design/business shows.business_show  business/show_business/business_show.js 

	# business template database - is replicated into new businesses in order to inherit apps
	./update_field.py -l $(cred) socialfarm_business_template _design/valid validate_doc_update validate_docs.js

	./update_field.py -l $(cred) socialfarm_business_template _design/scheduler views.offer_tasks.map scheduler/offer_tasks/map.js
	./update_field.py -l $(cred) socialfarm_business_template _design/scheduler views.offer_tasks.reduce scheduler/offer_tasks/reduce.js
	./update_field.py -l $(cred) socialfarm_business_template _design/scheduler views.pending_jobs_tasks.map scheduler/pending_jobs_tasks/map.js
	./update_field.py -l $(cred) socialfarm_business_template _design/scheduler views.pending_jobs_tasks.reduce scheduler/pending_jobs_tasks/reduce.js

	./update_field.py -l $(cred) socialfarm_business_template _design/info views.get_start_action.map info/get_start_action/map.js 
	./update_field.py -l $(cred) socialfarm_business_template _design/info views.list_members.map info/list_members/map.js
	./update_field.py -l $(cred) socialfarm_business_template _design/info views.list_actions.map info/list_actions/map.js 
	./update_field.py -l $(cred) socialfarm_business_template _design/info views.list_jobs.map info/list_jobs/map.js 
	./update_field.py -l $(cred) socialfarm_business_template _design/info views.list_tasks.map info/list_tasks/map.js

	./update_field.py -l $(cred) socialfarm_business_template _design/info lists.members_list info/list_members/members_list.js
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.members_list info/list_members/members_list.html 
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.members_list_row info/list_members/members_list_row.html

	./update_field.py -l $(cred) socialfarm_business_template _design/info lists.actions_list info/list_actions/actions_list.js
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.actions_list info/list_actions/actions_list.html 
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.actions_list_row info/list_actions/actions_list_row.html 

	./update_field.py -l $(cred) socialfarm_business_template _design/info lists.jobs_list info/list_jobs/jobs_list.js
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.jobs_list info/list_jobs/jobs_list.html 
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.jobs_list_row info/list_jobs/jobs_list_row.html

	./update_field.py -l $(cred) socialfarm_business_template _design/info lists.tasks_list info/list_tasks/tasks_list.js
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.tasks_list info/list_tasks/tasks_list.html 
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.tasks_list_row info/list_tasks/tasks_list_row.html

	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.member_show info/show_member/member_show.html 
	./update_field.py -l $(cred) socialfarm_business_template _design/info shows.member_show  info/show_member/member_show.js 

	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.action_show info/show_action/action_show.html 
	./update_field.py -l $(cred) socialfarm_business_template _design/info shows.action_show  info/show_action/action_show.js 

	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.job_show info/show_job_task/job_show.html 
	./update_field.py -l $(cred) socialfarm_business_template _design/info common.html.task_show info/show_job_task/task_show.html 
	./update_field.py -l $(cred) socialfarm_business_template _design/info shows.job_task_show  info/show_job_task/job_task_show.js 

clean: 
	./delete_database.py -l $(cred) testbus
	./delete_database.py -l $(cred) testbus2
	./delete_database.py -l $(cred) socialfarm_business_template
	./delete_database.py -l $(cred) socialfarm

test: 
	# create test businesses
	./SocialFarmHelper.py socialfarm success
