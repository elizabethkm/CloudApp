import os
from google.cloud import bigquery
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from sklearn.linear_model import LogisticRegression
from django.shortcuts import render
from django.http import HttpResponse
from .Forms import DataForm
from .Forms import DataForm2
from .models import Data
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.auth.transport import requests
from google.cloud.exceptions import NotFound


# Create your views here
def plot_view(request):
    start = time.time()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_json.json"
    deidentify_dataset('service_account_json.json', 'tempclouda', 'northamerica-northeast1', 'HealthCareData', 'DeId2')
    export_bigquery('service_account_json.json', 'tempclouda','northamerica-northeast1','DeId2', 'FHIRdata', 'tempclouda.queryDeId1')
    test_table_exists2()
    delete_dataset('service_account_json.json', 'tempclouda', 'northamerica-northeast1', 'DeId2')
    end = time.time()
    print("TIME PLOT:")
    print(end-start)
    return render(request, "polls/pic.html", {})

def predict_view(request):
    form = DataForm2(request.POST)
    prob = ""
    if form.is_valid():
        start = time.time()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_json.json"
        deidentify_dataset('service_account_json.json', 'tempclouda', 'northamerica-northeast1','HealthCareData', 'DeId2')
        export_bigquery('service_account_json.json', 'tempclouda', 'northamerica-northeast1', 'DeId2','FHIRdata', 'tempclouda.queryDeId1')
        prob = test_table_exists(form['Gender'].value(), form['ProcedureReason'].value())
        delete_dataset('service_account_json.json', 'tempclouda', 'northamerica-northeast1', 'DeId2')
        context = {
            'form': form, 'prob': prob
        }
        end = time.time()
        print("TIME PREDICT:")
        print(end - start)
        return render(request, "polls/predict.html", context)
    context = {
        'form': form
    }
    return render(request, "polls/predict.html", context)


def data_create_view(request):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/eliza/PycharmProjects/cloudproj/CloudApp/service_account_json.json"
    form = DataForm(request.POST)
    if form.is_valid():
        #form.save() #NO LONGER WANT TO USE CLOUD SQL
        resp, idP = create_resourcePatient('service_account_json.json', 'https://healthcare.googleapis.com/v1beta1',
                                           'tempclouda', 'northamerica-northeast1', 'HealthCareData',
                                           'FHIRdata', 'Patient', form['FirstName'].value(), form['LastName'].value(), form['Gender'].value())
        create_resourceProcedure('service_account_json.json', 'https://healthcare.googleapis.com/v1beta1', 'tempclouda',
                        'northamerica-northeast1', 'HealthCareData', 'FHIRdata', 'Procedure', form['ProcedureType'].value(), idP, form['ProcedureReason'].value(), form['ProcedureOutcome'].value(), form['DateOfBirth'].value())


    context = {
        'form' : form
    }

    #file = os.popen("service_account_json.json", 'r')
    #export_bigquery('service_account_json.json', 'tempclouda','northamerica-northeast1','DeId2', 'FHIRdata', 'tempclouda.queryDeId1')
    #delete_resource('service_account_json.json', 'https://healthcare.googleapis.com/v1beta1', 'tempclouda',
       #             'northamerica-northeast1', 'HealthCareData', 'FHIRdata', 'Procedure', '26ab3467-b378-4f2c-8804-3a9599ecc003' )
    #get_resource('service_account_json.json', 'https://healthcare.googleapis.com/v1beta1', 'tempclouda',
                # 'northamerica-northeast1', 'HealthCareData', 'FHIRdata', 'Procedure', 'b32fe1a1-aa55-45d2-b2c1-198e539377b1')
    #get_resource('service_account_json.json', 'https://healthcare.googleapis.com/v1beta1', 'tempclouda','northamerica-northeast1','DeId2', 'FHIRdata', 'Procedure', 'b32fe1a1-aa55-45d2-b2c1-198e539377b1')
    #low, high = calcAge('30-40')
    return render(request, "polls/data_create.html", context)


def get_client(service_account_json):
    """Returns an authorized API client by discovering the Healthcare API and
    creating a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1beta1'
    discovery_api = 'https://healthcare.googleapis.com/$discovery/rest'
    service_name = 'healthcare'

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?labels=CHC_BETA&version={}'.format(
        discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials)

def create_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id):
    """Creates a dataset."""
    client = get_client(service_account_json)
    dataset_parent = 'projects/{}/locations/{}'.format(
        project_id, cloud_region)

    body = {}

    request = client.projects().locations().datasets().create(
        parent=dataset_parent, body=body, datasetId=dataset_id)

    try:
        response = request.execute()
        print('Created dataset: {}'.format(dataset_id))
        return response
    except HttpError as e:
        print('Error, dataset not created: {}'.format(e))
        return ""
# [END healthcare_create_dataset]

def delete_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id):
    """Deletes a dataset."""
    client = get_client(service_account_json)
    dataset_name = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)

    request = client.projects().locations().datasets().delete(
        name=dataset_name)

    try:
        response = request.execute()
        print('Deleted dataset: {}'.format(dataset_id))
        return response
    except HttpError as e:
        print('Error, dataset not deleted: {}'.format(e))
        return ""

def get_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id):
    """Gets any metadata associated with a dataset."""
    client = get_client(service_account_json)
    dataset_name = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)

    datasets = client.projects().locations().datasets()
    dataset = datasets.get(name=dataset_name).execute()

    print('Name: {}'.format(dataset.get('name')))
    print('Time zone: {}'.format(dataset.get('timeZone')))

    return dataset

def create_fhir_store(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id):
    """Creates a new FHIR store within the parent dataset."""
    client = get_client(service_account_json)
    fhir_store_parent = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)

    body = {}

    request = client.projects().locations().datasets().fhirStores().create(
        parent=fhir_store_parent, body=body, fhirStoreId=fhir_store_id)

    try:
        response = request.execute()
        print('Created FHIR store: {}'.format(fhir_store_id))
        return response
    except HttpError as e:
        print('Error, FHIR store not created: {}'.format(e))
        return ""

def list_fhir_stores(service_account_json, project_id, cloud_region, dataset_id):
    """Lists the FHIR stores in the given dataset."""
    client = get_client(service_account_json)
    fhir_store_parent = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)

    fhir_stores = client.projects().locations().datasets().fhirStores().list(
        parent=fhir_store_parent).execute().get('fhirStores', [])

    for fhir_store in fhir_stores:
        print('FHIR store: {}\n'
              'Enable update/create: {}\n'
              'Notification config: {}\n'
              'Disable referential integrity: {}'.format(
                  fhir_store.get('name'),
                  fhir_store.get('enableUpdateCreate'),
                  fhir_store.get('notificationConfig'),
                  fhir_store.get('disableReferentialIntegrity')
              ))

    return fhir_stores

def create_resourcePatient(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type, firstIn, lastIn, genIn):
    """Creates a new resource in a FHIR store."""
    url = '{}/projects/{}/locations/{}'.format(base_url, project_id,
                                               cloud_region)

    fhir_store_path = '{}/datasets/{}/fhirStores/{}/fhir/{}'.format(
        url, dataset_id, fhir_store_id, resource_type)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }
    payload = {
        "resourceType": resource_type,
        "name": [
            {
                "given": [
                    firstIn,
                    lastIn
                ]
            }
        ],
        "gender": genIn
    }

    try:
        response = session.post(fhir_store_path, headers=headers, json=payload)
        response.raise_for_status()

        resource = response.json()

        print(
            'Created Resource: {} with ID {}'.format(
                resource_type,
                resource['id']))

        return response, resource['id']
    except HttpError as err:
        print(err)
        return ""

def create_resourceProcedure(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type, codeIn, subjectID, reasonCode, outcomeCode, dob) :#lowage, highage):
    """Creates a new resource in a FHIR store."""
    url = '{}/projects/{}/locations/{}'.format(base_url, project_id,
                                               cloud_region)

    fhir_store_path = '{}/datasets/{}/fhirStores/{}/fhir/{}'.format(
        url, dataset_id, fhir_store_id, resource_type)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }
    payload = {
        'resourceType': resource_type,
        "code": {
            "coding": [
                {
                    "code": codeIn,
                }
            ]
        },
        "subject": {
            "reference": "Patient/" + subjectID,
        },
        "reasonCode": [
            {
                "coding": [
                    {
                        "code": reasonCode
                    }
                ]
            }
        ],
        "outcome": {
            "coding": [
                {
                    "code": outcomeCode,
                }
            ]
        },
        "performedDateTime": dob #Don't use this! This is for date of procedure!
    }

    try:
        response = session.post(fhir_store_path, headers=headers, json=payload)
        response.raise_for_status()

        resource = response.json()

        print(
            'Created Resource: {} with ID {}'.format(
                resource_type,
                resource['id']))

        return response, resource['id']
    except HttpError as err:
        print(err)
        return ""

def get_session(service_account_json):
    """Returns an authorized Requests Session class using the service account
    credentials JSON. This class is used to perform requests to the
    Healthcare API endpoint."""

    # Pass in the credentials and project ID. If none supplied, get them
    # from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/cloud-platform'])

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    return session

def patch_fhir_store(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id):
    """Updates the FHIR store."""
    client = get_client(service_account_json)
    fhir_store_parent = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)
    fhir_store_name = '{}/fhirStores/{}'.format(
        fhir_store_parent, fhir_store_id)

    patch = {
        'enableUpdateCreate': True}

    request = client.projects().locations().datasets().fhirStores().patch(
        name=fhir_store_name, updateMask='enableUpdateCreate', body=patch)

    try:
        response = request.execute()
        print(
            'Patched FHIR store {} with Cloud Pub/Sub topic: None'.format(
                fhir_store_id))
        return response
    except HttpError as e:
        print('Error, FHIR store not patched: {}'.format(e))
        return ""

def delete_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id):
    """Deletes a FHIR resource or returns NOT_FOUND if it doesn't exist."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_path = '{}/datasets/{}/fhirStores/{}/resources/{}/{}'.format(
        url, dataset_id, fhir_store_id, resource_type, resource_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    try:
        response = session.delete(resource_path, headers=headers)
        if response.status_code != 404:  # Don't consider missing to be error
            response.raise_for_status()
        print(response)
        print('Deleted Resource: {}'.format(resource_id))
        return response
    except HttpError:
        print('Error, Resource not deleted')
        return ""
# [END healthcare_delete_resource]

def list_resource_history(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id):
    """Gets the history of a resource."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_path = '{}/datasets/{}/fhirStores/{}/fhir/{}/{}'.format(
        url, dataset_id, fhir_store_id, resource_type, resource_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    response = session.get(resource_path + '/_history', headers=headers)
    response.raise_for_status()

    resource = response.json()

    print(json.dumps(resource, indent=2))

    return resource

def get_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id):
    """Gets a FHIR resource."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_path = '{}/datasets/{}/fhirStores/{}/fhir/{}/{}'.format(
        url, dataset_id, fhir_store_id, resource_type, resource_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    response = session.get(resource_path, headers=headers)
    response.raise_for_status()

    resource = response.json()

    print(json.dumps(resource, indent=2))

    return resource

def deidentify_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        destination_dataset_id):
    """Creates a new dataset containing de-identified data
    from the source dataset.
    """
    client = get_client(service_account_json)
    source_dataset = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)
    destination_dataset = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, destination_dataset_id)

    body = {
        'destinationDataset': destination_dataset,
        'config': {
            'fhir': {}
        }
    }

    request = client.projects().locations().datasets().deidentify(
        sourceDataset=source_dataset, body=body)

    try:
        response = request.execute()
        print(
            'Data in dataset {} de-identified.'
            'De-identified data written to {}'.format(
                dataset_id,
                destination_dataset_id))
        return response
    except HttpError as e:
        print('Error, data could not be deidentified: {}'.format(e))
        return ""

def calcAge(range):
    ages = range.split('-', 1)
    low = int(ages[0])
    high = int(ages[1])
    return low, high

def export_bigquery(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        gcs_uri):
    """Export resources to a Google Cloud Storage bucket by copying
    them from the FHIR store."""
    client = get_client(service_account_json)
    fhir_store_parent = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)
    fhir_store_name = '{}/fhirStores/{}'.format(
        fhir_store_parent, fhir_store_id)

    body = {
        'bigqueryDestination': {
            'datasetUri': 'bq://{}'.format(gcs_uri)
        }
    }

    request = client.projects().locations().datasets().fhirStores().export(
        name=fhir_store_name, body=body)

    try:
        response = request.execute()
        print('Exported FHIR resources to bucket: bq://{}'.format(gcs_uri))
        return response
    except HttpError as e:
        print('Error, FHIR resources not exported: {}'.format(e))
        return ""


def test_table_exists2():
    """Determine if a table exists."""
    client = bigquery.Client()
    DATASET_ID = "queryDeId1"
    tables = client.list_tables(DATASET_ID)
    patTable = "Filler"
    proTable = "Warning"
    for table in tables:
        if (table.table_id.startswith('Patient')):
            patTable = table.table_id
        else:
            proTable = table.table_id
    TABLE_ID = proTable
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    table_ref = dataset.table(TABLE_ID)
    try:
        a = client.get_table(table_ref)
    except NotFound:
        return False
    sql = """
        SELECT b.patient.gender.value, a.procedure.code, a.procedure.outcome, a.procedure.reasonCode
        FROM queryDeId1.%s as a, queryDeId1.%s as b
        WHERE b.patient.id.value = a.procedure.subject.patientId.value;
    """ % (proTable, patTable)
    df = client.query(sql).to_dataframe()
    df['code'] = df['code'].apply(lambda x: x.get('coding')[0].get('code').get('value'))
    df['outcome'] = df['outcome'].apply(lambda x: x.get('coding')[0].get('code').get('value'))
    df['reasonCode'] = df['reasonCode'].apply(lambda x: (x[0]))
    df['reasonCode'] = df['reasonCode'].apply(lambda x: x.get('coding')[0].get('code').get('value'))
    df['outcome'] = df.outcome.map({'385669000': 0}).fillna(1).astype(int)
    df['value'] = df.value.map({'MALE': 0}).fillna(1).astype(int)
    data1 = df.groupby('reasonCode').mean()[['outcome']]
    data1['outcome'] = data1['outcome'].apply(lambda x: (1 - x) * 100)
    counts = df.groupby('reasonCode').count().sort_values(by=['outcome'])
    rC = ['2470005', '2776000', '3119002', '4069002']
    sR = [data1.loc['2470005'][0], data1.loc['2776000'][0], data1.loc['3119002'][0], data1.loc['4069002'][0]]
    index = ['Brain damage', 'Organic brain syndrome', 'Brain stem laceration', 'Anoxic brain damage']
    df1 = pd.DataFrame({'ReasonCode': rC, 'Rate of Success': sR}, index=index)
    ax = df1.plot.bar(title='Success Rate(%) For ReasonCodes', rot=10)
    ax.set_ylabel('Success Rate (%)')
    fig = ax.get_figure()
    fig.savefig('static/reasoncode.png')

    client.delete_dataset('tempclouda.queryDeId1', delete_contents=True, not_found_ok=True)
    dataset = bigquery.Dataset('tempclouda.queryDeId1')
    dataset.location = "US"
    dataset = client.create_dataset(dataset)  # API request
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

def test_table_exists(gender_code, r_code):
    """Determine if a table exists."""
    client = bigquery.Client()
    DATASET_ID = "queryDeId1"
    tables = client.list_tables(DATASET_ID)
    patTable = "Filler"
    proTable = "Warning"
    for table in tables:
        if(table.table_id.startswith('Patient')):
            patTable = table.table_id
        else:
            proTable = table.table_id
    print(proTable)
    print(patTable)
    sql = """
        SELECT b.patient.gender.value, a.procedure.code, a.procedure.outcome, a.procedure.reasonCode
        FROM queryDeId1.%s as a, queryDeId1.%s as b
        WHERE b.patient.id.value = a.procedure.subject.patientId.value;
    """ % (proTable, patTable)
    df = client.query(sql).to_dataframe()
    df['code'] = df['code'].apply(lambda x: x.get('coding')[0].get('code').get('value'))
    df['outcome'] = df['outcome'].apply(lambda x: x.get('coding')[0].get('code').get('value'))
    df['reasonCode'] = df['reasonCode'].apply(lambda x: (x[0]))
    df['reasonCode'] = df['reasonCode'].apply(lambda x: x.get('coding')[0].get('code').get('value'))
    df['outcome'] = df.outcome.map({'385669000': 0}).fillna(1).astype(int)
    df['value'] = df.value.map({'MALE': 0}).fillna(1).astype(int)
    data1 = df.groupby('reasonCode').mean()[['outcome']]
    data1['outcome'] = data1['outcome'].apply(lambda x: (1 - x) * 100)
    counts = df.groupby('reasonCode').count().sort_values(by=['outcome'])
    rC = ['2470005', '2776000', '3119002', '4069002']
    sR = [data1.loc['2470005'][0], data1.loc['2776000'][0], data1.loc['3119002'][0], data1.loc['4069002'][0]]
    index = ['Brain damage', 'Organic brain syndrome', 'Brain stem laceration','Anoxic brain damage']
    df1 = pd.DataFrame({'ReasonCode': rC, 'Rate of Success': sR}, index=index)
    ax = df1.plot.bar(title='Success Rate(%) For ReasonCodes', rot = 10)
    ax.set_ylabel('Success Rate (%)')
    fig = ax.get_figure()
    fig.savefig('static/reasoncode.png')

    new_data = df.drop(['outcome', 'code'], axis=1)
    out = df['outcome']
    lm = LogisticRegression().fit(new_data, out)
    test = pd.DataFrame(columns=['value', 'reasonCode'])
    if(gender_code == 'male'):
        gender_code = 0
    else:
        gender_code = 1
    test = test.append({'value': gender_code, 'reasonCode': r_code}, ignore_index=True)
    qual = lm.predict_proba(test)
    prob = qual[0][0]
    print(prob)
    client.delete_dataset('tempclouda.queryDeId1', delete_contents=True, not_found_ok=True)
    dataset = bigquery.Dataset('tempclouda.queryDeId1')
    dataset.location = "US"
    dataset = client.create_dataset(dataset)  # API request
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
    return prob*100
    #delete DEID2
