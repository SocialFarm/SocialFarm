CREDENTIALS 	= socialfarm:success

UPDATE_BUSINESS = ./scripts/update_field.py socialfarm                    _design/business
UPDATE_INFO 	= ./scripts/update_field.py socialfarm_business_template  _design/info
UPDATE_SCHED    = ./scripts/update_field.py socialfarm_business_template  _design/scheduler
UPDATE_VALID    = ./scripts/update_field.py socialfarm_business_template  _design/valid

all : clean install_common install_business install_info install_scheduler install_social_news

install_common :
	$(UPDATE_INFO)		js.common.mustache 		            common/js/mustache.js 
	$(UPDATE_INFO)		js.common.potato 	                common/js/potato.js 
	$(UPDATE_INFO)		html.common.base 		            common/html/base.html
	$(UPDATE_INFO) 		html.common.default_js 	            common/html/default_js.html 
	$(UPDATE_INFO) 		html.common.default_css             common/html/default_css.html 
	$(UPDATE_INFO) 		html.common.header 		            common/html/header.html 
	$(UPDATE_INFO) 		html.common.business_navigation 	common/html/business_navigation.html 
	$(UPDATE_INFO) 		html.common.user_navigation 	    common/html/user_navigation.html
	$(UPDATE_INFO) 		html.common.content 	            common/html/content.html 
	$(UPDATE_INFO) 		html.common.footer 		            common/html/footer.html 
	$(UPDATE_BUSINESS)	js.common.mustache 		            common/js/mustache.js 
	$(UPDATE_BUSINESS)	js.common.potato 	                common/js/potato.js 
	$(UPDATE_BUSINESS)	html.common.base 		            common/html/base.html 
	$(UPDATE_BUSINESS) 	html.common.default_css             common/html/default_css.html
	$(UPDATE_BUSINESS) 	html.common.default_js 	            common/html/default_js.html
	$(UPDATE_BUSINESS) 	html.common.header 		            common/html/header.html
	$(UPDATE_BUSINESS) 	html.common.business_navigation 	common/html/business_navigation.html
	$(UPDATE_BUSINESS) 	html.common.user_navigation 	    common/html/user_navigation.html
	$(UPDATE_BUSINESS) 	html.common.content 	            common/html/content.html
	$(UPDATE_BUSINESS) 	html.common.footer 		            common/html/footer.html

install_business :
	#views
	$(UPDATE_BUSINESS) 	views.all_businesses.map  	        business/views/all_businesses.js
	$(UPDATE_BUSINESS) 	views.my_tasks.map  	            business/views/my_businesses.js	
	$(UPDATE_BUSINESS) 	views.my_businesses.map             business/views/my_businesses.js

	#shows
	$(UPDATE_BUSINESS) 	shows.business 			            business/shows/business.js 
	$(UPDATE_BUSINESS) 	shows.join_business 	            business/shows/join_business.js
	$(UPDATE_BUSINESS) 	shows.my_businesses 	            business/shows/my_businesses.js
	$(UPDATE_BUSINESS) 	shows.my_tasks 			            business/shows/my_tasks.js

	$(UPDATE_BUSINESS) 	html.business 			            business/shows/business.html  
	$(UPDATE_BUSINESS) 	html.join_business 		            business/shows/join_business.html 
	$(UPDATE_BUSINESS) 	html.my_businesses 		            business/shows/my_businesses.html 
	$(UPDATE_BUSINESS) 	html.my_tasks 			            business/shows/my_tasks.html 

	#lists
	$(UPDATE_BUSINESS) 	lists.businesses 		            business/lists/businesses.js 

	$(UPDATE_BUSINESS) 	html.businesses			            business/lists/businesses.html 
	$(UPDATE_BUSINESS) 	html.businesses_row 	            business/lists/businesses_row.html 

install_info :
	#views 
	$(UPDATE_INFO) 		views.get_start_action.map 	        info/views/get_start_action.js 
	$(UPDATE_INFO) 		views.all_members.map 			    info/views/all_members.js
	$(UPDATE_INFO) 		views.all_activities.map 		    info/views/all_activities.js 
	$(UPDATE_INFO) 		views.all_jobs.map 				    info/views/all_jobs.js 
	$(UPDATE_INFO) 		views.all_tasks.map 			    info/views/all_tasks.js

	#shows
	$(UPDATE_INFO) 		shows.member 				        info/shows/member.js
	$(UPDATE_INFO) 		shows.activity 				        info/shows/activity.js
	$(UPDATE_INFO) 		shows.job 					        info/shows/job.js
	$(UPDATE_INFO) 		shows.task					        info/shows/task.js

	$(UPDATE_INFO) 		html.member 				        info/shows/member.html  
	$(UPDATE_INFO) 		html.activity 				        info/shows/activity.html  
	$(UPDATE_INFO) 		html.job 					        info/shows/job.html  
	$(UPDATE_INFO) 		html.task	 				        info/shows/task.html  

	#lists
	$(UPDATE_INFO) 		lists.members 		                info/lists/members.js
	$(UPDATE_INFO) 		lists.activities 	                info/lists/activities.js
	$(UPDATE_INFO) 		lists.jobs 			                info/lists/jobs.js
	$(UPDATE_INFO) 		lists.tasks 		                info/lists/tasks.js

	$(UPDATE_INFO) 		html.tasks 			                info/lists/tasks.html 
	$(UPDATE_INFO) 		html.tasks_row 		                info/lists/tasks_row.html

	$(UPDATE_INFO) 		html.jobs 			                info/lists/jobs.html 
	$(UPDATE_INFO) 		html.jobs_row 		                info/lists/jobs_row.html

	$(UPDATE_INFO) 		html.activities 	                info/lists/activities.html 
	$(UPDATE_INFO) 		html.activities_row                 info/lists/activities_row.html

	$(UPDATE_INFO) 		html.members 		                info/lists/members.html 
	$(UPDATE_INFO) 		html.members_row 	                info/lists/members_row.html
	
install_scheduler : 
	$(UPDATE_SCHED)	    views.offer_tasks.map 				scheduler/offer_tasks/map.js
	$(UPDATE_SCHED)	 	views.offer_tasks.reduce 			scheduler/offer_tasks/reduce.js
	$(UPDATE_SCHED)	 	views.pending_jobs_tasks.map 		scheduler/pending_jobs_tasks/map.js
	$(UPDATE_SCHED)	 	views.pending_jobs_tasks.reduce 	scheduler/pending_jobs_tasks/reduce.js
	$(UPDATE_VALID)	    validate_doc_update 				validate_docs.js

clean: 
	./scripts/delete_database.py testbus
	./scripts/delete_database.py testbus2
	./scripts/delete_database.py social_news
	./scripts/delete_database.py social_plumbing
	./scripts/delete_database.py socialfarm_business_template
	./scripts/delete_database.py socialfarm


install_social_news: 
	./scripts/SocialFarmHelper.py socialfarm success
	./scripts/SocialNews.py socialfarm success

