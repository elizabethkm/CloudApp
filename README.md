# CloudApp
Cloud Computing Term Project

#Deployed app visible at:

 [https://prefab-shape-235820.appspot.com]
 Note: The Plot visualization is not dynamically changing on the deployed version
 To reflect changes from the code in the repo(which is for running locally) to see what is deployed, follow the following steps:
 1. Change Settings.py to imitate this:
	     STATIC_ROOT="static"
	
      #STATICFILES_DIRS=[
      #os.path.join(BASE_DIR,"static"),
      #]
	
2. In views.py:
      In both test_table_exists and test_table_exits2:
            Ensure "#fig.savefig('static/reasoncode.png')"  is commented
Note: Errors of not found in US cause dataset issues which should be resolved by refreshing the page to instigate deletion of tables/datasets

#Running locally:



