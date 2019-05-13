# CloudApp
Cloud Computing Term Project

## Deployed app visible at:

 [https://tempclouda.appspot.com]
 
 Note: The Plot visualization is not dynamically changing on the deployed version. Everything else is the same! Prediction works.
 
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
[4. Install [CloudSQLproxy](https://cloud.google.com/sql/docs/mysql/connect-admin-proxy)]-> no longer need to do this! took out cloudsql so its easier to setup!
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

## Exploring the Code:

- Many functions used were taken from Google's online resources/samples for properly utlizing APIs

- Polls/views.py contains the bulk of the code

- To help understand the approach, an overview is listed below:

1. First the user is directed to "data_create_view". Here they can submit a form which contains Patient Information. When the click submit the following is executed
	
   - You create a Patient resource (which is just one patient entry) in our FHIRstore in our HealthCareData dataset through the HealthCareAPI
		
   - Since our app deals with two resources, Patient and Procedure, we immediately create a Procedure resource using the same subject_id we generated from the Patient resource in order to tell our dataset that these two resources correspond to the same "person". 
		
2. After they submit the form and the code is executed for a valid form on "data_create_view", they are routed back to the same page so they can again input another patient's entry
	
3. However, on ["data_create_view"](/https://prefab-shape-235820.appspot.com/) if users click Submit, they will be routed to "plot_view"/pic.html which does the following code:
	
     i . Deidentifies the HealthCareData dataset and creates DeId2 dataset (all through the HealthCareAPI)
		
     ii . Exports DeId2 to BigQuery. To do this, it creates 2 tables. One for the Patient resource and one for the Procedure resource. For our purposes, you can think of the Patient table as a list of patients entered into the form which holds gender. And Procedure table has the same list of patients but holds information such as "ProcedureReason", "ProcedureOutcome", etc.
		
     iii . Calls "test_table_exists2()" which gets the tables you just added to BigQuery and performs a SQL query to create one table with all the needed information. Then execute python code to calculate the [plot](https://prefab-shape-235820.appspot.com/plot?) and [prediction](https://prefab-shape-235820.appspot.com/predict?) that users see on the frontend.
		
      - Important Note: on deployed app we are using a static file which is read-only so we can't display the plot which truly corresponds to the most recently inputted data although we ARE calculating the computation steps which is why it takes so long to load. The image is just not saving during deployment, so it doesn't change. 
			
      - However, when we run locally, our plot is working perfectly! Therefore, it will reflect any changes due to recently inputted patient information
			
    iv. We also delete the dataset we created on BigQuery each time we call test_table_exists so that we don't run into problems trying to call it again and get new tables. As a result, we immediately create a new empty dataset on BigQuery for future exports.
		
     v. Delete the DeId2 dataset so you can perform the previous steps without any collisions
		
4. If user clicks "Input Data to Predict Success Rate" we go to polls/views/predict_view which replicates plot_view except that it calls test_table_exists which also calculates a LogisticRegression prediction and displays it to the user after they submit information needed to predict the success rate of selected features based on our "test" set which is our whole queried dataset from BigQuery. 

	



