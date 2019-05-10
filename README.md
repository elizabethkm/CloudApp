# CloudApp
Cloud Computing Term Project

## Deployed app visible at:

 [https://prefab-shape-235820.appspot.com]
 Note: The Plot visualization is not dynamically changing on the deployed version
 Note: Errors of not found in US cause dataset issues which should be resolved by *refreshing* the page to instigate deletion of tables/datasets
 To reflect changes from the code in the repo(which is for running locally) to see what is deployed, follow the following steps:
 1. Change Settings.py to imitate this:
	     STATIC_ROOT="static"
	
      #STATICFILES_DIRS=[
      #os.path.join(BASE_DIR,"static"),
      #]
	
2. In views.py:
      In both test_table_exists and test_table_exits2:
            Ensure "#fig.savefig('static/reasoncode.png')"  is commented


## Running locally:

1. Make sure python and pip is installed
2. Install Django within a virtualenv (We used PyCharm to setup the application)
	- Make sure all imports used in code are installed (Pandas, Matplotlib, etc)
3. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/#windows)
4. Install [CloudSQLproxy](https://cloud.google.com/sql/docs/mysql/connect-admin-proxy)
5. How we [authenticated](https://cloud.google.com/healthcare/docs/how-tos/authentication) to the HealthCare API:
- Obtained a service account key file which is named "service_account_json.json" in the repo
- Setting the environment variables: (Google's instructions listed below)
	- We included it in our code (polls/views.py) and did not need to set the enviornment each time
	* You can provide authentication credentials to your application code or commands by setting the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key.

	* Note that, if you are running your application on App Engine, you only need to set the GOOGLE_APPLICATION_CREDENTIALS environment variable if you are using a service account other than the default service account that those services provide.

	* The [samples](https://cloud.google.com/healthcare/docs/how-tos/authentication#healthcare-set-adc-cli-powershell) show how to set the GOOGLE_APPLICATION_CREDENTIALS environment variable

6. To actually run the code:

	1. 
		- For Mac: ./cloud_sql_proxy -instances=prefab-shape-235820:us-east1:cloudbase=tcp:3306
		- For Windows: cloud_sql_proxy.exe -instances=prefab-shape-235820:us-east1:cloudbase=tcp:3306
	2. In a new terminal, run "python manage.py runserver"



	



