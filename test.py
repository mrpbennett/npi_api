import npi_class as n
import config as c
import pandas as pd
import json
import time
import requests
from progress.bar import Bar
from simple_chalk import chalk

c = c.Config()
n = n.NPIListApi(c.username, c.password)


def progress_bar():
    with Bar(f"Please wait!", fill="🟪", max=301, suffix='%(percent)d%%') as bar:
        for _ in range(301):
            time.sleep(1)
            bar.next()

"""
1. get_npi_list method:

JL_Xospata Proj Evolve - Entire List - Seg A - from PP Tech Solutions
List ID: 5547
"""

# n.get_npi_list('data', 5547)

"""
2. GET ALL NPI LISTS
account_id = 561939
"""

# n.get_all_npi_lists(561939)

"""
3. create_npi_list method:

CREATE NPI list for PP Tech Solutions. 
Acct ID - 561939
"""

#n.create_npi_list(561939)

"""
4. replace_npi_list method:

REPLACE list for PP Tech Solutions. 
LIST ID - 8855
"""
n.replace_npi_list(8855)

"""
5. add_npi_to_lists method:

ADD NPI to list for PP Tech Solutions. 
LIST ID - 8855
"""
#n.add_npi_to_list(8855)

"""
6. delete_npi_from_list method:

ADD NPI to list for PP Tech Solutions. 
LIST ID - 8855
"""
#n.delete_npi_from_list(8855)

# testing out the df process
new_lists = []

''' CREATE NPI LIST TEST '''

# df = pd.read_csv('data/create_npi_lists/npi_test_single.csv')[['TargetListID', 'NPI_ID']]
# df = pd.read_csv('./data/create_npi_lists/npi_test.csv')[['TargetListID', 'NPI_ID']]
# df = df.dropna()
#
# for target in df['TargetListID'].unique():
#     new_list = df[df['TargetListID'] == target].reset_index(drop=True)
#     new_list = new_list['NPI_ID'].apply(lambda x: str(int(x))).to_list()
#
#     if len(new_list) > 1000000:
#         print(chalk.red('❌ One of the lists is above our MAX of 1,000,000 NPIs, please reduce the list!'))
#         break
#
#     else:
#         final_list = dict(name=target, npis=new_list)
#         new_lists.append(final_list)
#
#     print(f'final_list is: \n {json.dumps(final_list, indent=2)}')
#     print(f'new_lists holds: \n {json.dumps(new_lists, indent=2)}')
#
# print(f'We have detected {len(new_lists)} list/s to be created this could take {len(new_lists) * 300 / 60} mins or more to upload \n')
#
# try:
#     for i, v in enumerate(new_lists):
#         r = requests.post('https://httpbin.org/post', json=json.dumps(v))
#         r.raise_for_status()
#
#         if r.status_code == requests.codes.ok:
#             progress_bar()
#             print(f'List #{i + 1} uploaded 👍')
#
# except requests.exceptions.HTTPError as err:
#     raise SystemExit(err)


""" REPLACE NPI TEST """

df = pd.read_csv('./data/create_npi_lists/npi_test_single.csv')[['TargetListID', 'NPI_ID']]
df = df.dropna()

for target in df['TargetListID'].unique():
    new_list = df[df['TargetListID'] == target].reset_index(drop=True)
    new_list = new_list['NPI_ID'].apply(lambda x: str(int(x))).to_list()

    if len(new_list) > 1000000:
        print(chalk.red('❌ One of the lists is above our MAX of 1,000,000 NPIs, please reduce the list!'))
        break
    else:
        final_list = dict(npis=new_list)

    print(f'final_list is: \n {json.dumps(final_list, indent=2)}')

print(f'We have detected {len(new_lists)} list/s to be created this could take {len(new_lists) * 300 / 60} mins or more to upload \n')

try:
        r = requests.put('https://httpbin.org/put', json=json.dumps(final_list))
        r.raise_for_status()

        if r.status_code == requests.codes.ok:
            progress_bar()
            print(f'Your NPIs have been REPLACED 👍')

except requests.exceptions.HTTPError as err:
    raise SystemExit(err)


''' ADD NPI TEST '''

# df = pd.read_csv('data/add_npi_to_lists/npi_test.csv')[['TargetListID', 'NPI_ID']]
# df = df.dropna()
#
# for target in df['TargetListID'].unique():
#     new_list = df[df['TargetListID'] == target].reset_index(drop=True)
#     new_list = new_list['NPI_ID'].apply(lambda x: str(int(x))).to_list()
#
#     if len(new_list) > 1000000:
#         print(chalk.red('❌ One of the lists is above our MAX of 1,000,000 NPIs, please reduce the list!'))
#         break
#     else:
#         final_list = dict(operation="add", npis=new_list)
#
#     print(f'final_list is: \n {json.dumps(final_list, indent=2)}')
#
# print(f'We have detected {len(new_lists)} list/s to be created this could take {len(new_lists) * 300 / 60} mins or more to upload \n')
#
# try:
#         r = requests.patch('https://httpbin.org/patch', json=json.dumps(final_list))
#         r.raise_for_status()
#
#         if r.status_code == requests.codes.ok:
#             progress_bar()
#             print(f'Your NPIs have been ADDED to 1234 👍')
#
# except requests.exceptions.HTTPError as err:
#     raise SystemExit(err)

''' DELETE NPI TEST '''

# df = pd.read_csv('data/add_npi_to_lists/npi_test.csv')[['TargetListID', 'NPI_ID']]
# df = df.dropna()
#
# for target in df['TargetListID'].unique():
#     new_list = df[df['TargetListID'] == target].reset_index(drop=True)
#     new_list = new_list['NPI_ID'].apply(lambda x: str(int(x))).to_list()
#
#     if len(new_list) > 1000000:
#         print(chalk.red('❌ One of the lists is above our MAX of 1,000,000 NPIs, please reduce the list!'))
#         break
#     else:
#         final_list = dict(operation="remove", npis=new_list)
#         print(final_list)
#
# try:
#     r = requests.patch(f"https://httpbin.org/patch", json=final_list)
#     r.raise_for_status()
#
#     if r.status_code == requests.codes.ok:
#         progress_bar()
#         print(f'Your NPIs have been REMOVED from 12345 👍')
#
# except requests.exceptions.HTTPError as err:
#     raise SystemExit(err)