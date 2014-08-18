ifneq ($(SF_USERNAME),)
ifneq ($(SF_PASSWORD),)
	CREDENTIALS = -l $(SF_USERNAME):$(SF_PASSWORD) 
endif
endif


#####
## !!! WARNING 
## notice that expansion of these variables can cause bugs because
## if terminating space is absent, two args will be combined: eg: 
## _design/business><html.common.user_navigation 
#####


UPDATE_INFO 	= ./scripts/update_field.py $(CREDENTIALS) social_ride  _design/info   
UPDATE_SCHED    = ./scripts/update_field.py $(CREDENTIALS) social_ride  _design/scheduler   
UPDATE_VALID    = ./scripts/update_field.py $(CREDENTIALS) social_ride  _design/valid   


all : clean  install_info install_scheduler install_social_ride 
	@echo Done

install_info :
#views 
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
	$(UPDATE_INFO) 		lists.tasks 		                info/lists/tasks.js

	$(UPDATE_INFO) 		html.tasks 			                info/lists/tasks.html 
	$(UPDATE_INFO) 		html.tasks_row 		                info/lists/tasks_row.html

	$(UPDATE_INFO) 		html.activities 	                info/lists/activities.html 
	$(UPDATE_INFO) 		html.activities_row                 info/lists/activities_row.html

	$(UPDATE_INFO) 		html.members 		                info/lists/members.html 
	$(UPDATE_INFO) 		html.members_row 	                info/lists/members_row.html
# css file attachments
	./scripts/attachments.py social_ride _design/info facebook.css info/css/facebook.css
	./scripts/attachments.py social_ride _design/info base.css info/css/base.css
	./scripts/attachments.py social_ride _design/info reset.css info/css/reset.css
	./scripts/attachments.py social_ride _design/info style.css info/css/style.css
	./scripts/attachments.py social_ride _design/info map.css info/css/map.css
	./scripts/attachments.py social_ride _design/info logo.png info/images/logo.png
	./scripts/attachments.py social_ride _design/info image.jpg info/images/image.jpg
	./scripts/attachments.py social_ride _design/info close.jpg info/images/close.jpg
	./scripts/attachments.py social_ride _design/info graybar_top.png info/images/graybar_top.png
	./scripts/attachments.py social_ride _design/info graybar_bottom.png info/images/graybar_bottom.png

install_scheduler : 
	$(UPDATE_SCHED)	    views.offer_tasks.map 				scheduler/offer_tasks/map.js
	$(UPDATE_SCHED)	 	views.offer_tasks.reduce 			scheduler/offer_tasks/reduce.js
	$(UPDATE_SCHED)	 	views.pending_jobs_tasks.map 		scheduler/pending_jobs_tasks/map.js
	$(UPDATE_SCHED)	 	views.pending_jobs_tasks.reduce 	scheduler/pending_jobs_tasks/reduce.js
	$(UPDATE_VALID)	    validate_doc_update 				validate_docs.js


clean: 
ifeq ($(CREDENTIALS),) 
	$(error shell variables SF_USERNAME and/or SF_PASSWORD undefined)		
endif
	./scripts/delete_database.py $(CREDENTIALS) social_ride
	

install_social_ride:
	./scripts/update_field.py $(CREDENTIALS) social_ride _design/info views.nearby_jobs.map socialride/nearby_jobs/map.js
	./scripts/update_field.py $(CREDENTIALS) social_ride _design/info views.nearby_request.map socialride/nearby_jobs/map_request.js
	./scripts/update_field.py $(CREDENTIALS) social_ride _design/info views.nearby_offer.map socialride/nearby_jobs/map_offer.js

