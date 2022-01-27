from authlib.integrations.requests_client import OAuth2Session
from simple_chalk import chalk
from progress.bar import Bar
import pandas as pd
import requests
import json
import time
import config
import urllib3

# disable urllib3 warnings
urllib3.disable_warnings()

c = config.Config()


class NPIListApi:
    # global variables for the class
    auth_url = c.url
    client_id = c.client_id
    client_secret = c.client_secret

    def __init__(self, username, password):
        self.username = username
        self.password = password

    """ Method to establish connection to the LIFE API """

    def establish_connection(self):
        # Fetch an access token from the provider.
        client = OAuth2Session(self.client_id, self.client_secret)
        token = client.fetch_token(self.auth_url, authorization_response=self.auth_url,
                                   username=self.username, password=self.password, grant_type='password')

        # establish a new client with the token we got above
        client = OAuth2Session(self.client_id, self.client_secret, token=token)

        return client

    """ 
    This method requires the user to add the FILE LOCATION PART and the LIST ID of the list they need exporting
    as an argument. The file location can be a path like so folder/folder
    example: class_instance.export_npi_list_to_csv("./data", 1234)
    """

    def get_npi_list(self, file_loc, list_id):

        conn = self.establish_connection()

        try:
            r = conn.get(f"https://lifeapi.pulsepoint.com/RestApi/v1/npi/npi-list/{list_id}")
            r.raise_for_status()

            # This GETS NPI list from url and puts it into a CSV file
            if r.status_code == requests.codes.ok:
                # convert json into a string
                data_str = json.dumps(r.json())

                # places json string into a dataframe
                df = pd.read_json(data_str)

                # creates a csv file from dataframe and stores it locally
                print(chalk.green(f'SUCCESS! NPI List ID {list_id} has been exported to {file_loc}/'))
                return df.to_csv(f'{file_loc}/npi_list_{list_id}.csv', index=False)

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    """
    This method allows the user to generate a JSON object of all the NPIs lists associated with their account. 
    User would need to supply the ACCOUNT ID of the account they wish to check.
    example: class_instance.get_all_npi_lists(561939)
    """

    def get_all_npi_lists(self, account_id):
        conn = self.establish_connection()

        try:
            r = conn.get(f"https://lifeapi.pulsepoint.com/RestApi/v1/npi/npi-list/account/{account_id}")
            r.raise_for_status()

            if r.status_code == requests.codes.ok:
                print(chalk.green(f'SUCCESS! Here are your NPI lists.'))
                print(json.dumps(r.json(), indent=1))

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)


    """
    Create a list from a .csv file stored in a certain directory and send it into LIFE. User would need to supply the
    ACCOUNT ID of the account they wish to create the list within.
    example: class_instance.create_npi_list(561939)
    
    We need to send JSON to client in the format of:
    
    {
        "name": "test",
        "npis" [
            "123456",
            "123456",
            "122345",
            ...
        ]
    }
    """

    def create_npi_list(self, account_id):

        new_lists = []

        conn = self.establish_connection()

        # ingest data from ./data/test - storing only cols TargetListID & NPI_ID
        df = pd.read_csv('./data/test/npi_test.csv')[['TargetListID', 'NPI_ID']]
        df = df.dropna()

        # here we loop through original df to get unique IDs and NPIs then sort into separate dicts
        for target in df['TargetListID'].unique():
            new_list = df[df['TargetListID'] == target].reset_index(drop=True)
            new_list = new_list['NPI_ID'].apply(lambda x: str(int(x))).to_list()

            # final_list is the dict we pass into new_lists so we can send this to our api
            final_list = dict(name=target, npis=new_list)
            new_lists.append(final_list)

        print(f'We have detected {len(new_lists)} lists to be created this could take {len(new_lists)} '
              f'min/s or more to upload \n')

        try:
            # loop through new_lists and send list to npis
            for i, list in enumerate(new_lists):
                r = conn.post(f'https://lifeapi.pulsepoint.com/RestApi/v1/npi/npi-list/account/{account_id}',
                              json=list, verify=False)
                r.raise_for_status()

                if r.status_code == requests.codes.ok:
                    self.progress_bar()
                    print(f'List #{i + 1} uploaded 👍')

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    """
    Replace NPIs within a list. User would need to supply the LIST ID of the list where they wish to replace NPIs 
    example: class_instance.replace_npi_list(123456)
    """

    def replace_npi_list(self, list_id):

        conn = self.establish_connection()

        try:
            r = conn.put(f"https://lifeapi.pulsepoint.com/RestApi/v1/npi/npi-list/{list_id}")
            r.raise_for_status()

            if r.status_code == requests.codes.ok:
                pass

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    """
    Add NPIs to a list within LIFE. User would need to supply the LIST ID of the list where they wish to ADD NPIs too
    example: class_instance.add_npi_to_list(123456)
    """

    def add_npi_to_list(self, list_id):

        conn = self.establish_connection()

        try:
            r = conn.patch(f"https://lifeapi.pulsepoint.com/RestApi/v1/npi/npi-list/{list_id}")
            r.raise_for_status()

            if r.status_code == requests.codes.ok:
                pass

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    """
    DELETE NPIs from a list within LIFE. User would need to supply the LIST ID of the list where they wish to DELETE 
    NPIs from. 
    example: class_instance.delete_npi_from_list(123456)
    """

    def delete_npi_from_list(self, list_id):

        conn = self.establish_connection()

        try:
            r = conn.patch(f"https://lifeapi.pulsepoint.com/RestApi/v1/npi/npi-list/{list_id}")
            r.raise_for_status()

            if r.status_code == requests.codes.ok:
                pass

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    """ Timer function to prevent overloading of the API. This timer is set for 60 secs """

    @staticmethod
    def progress_bar():
        with Bar(f"Uploading!", fill="🟪", max=61, suffix='%(percent)d%%') as bar:
            for _ in range(61):
                time.sleep(1)
                bar.next()
