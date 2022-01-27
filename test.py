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
    with Bar(f"Uploading!", fill="🟪", max=60, suffix='%(percent)d%%') as bar:
        for _ in range(60):
            time.sleep(1)
            bar.next()

"""
get_npi_list method:

JL_Xospata Proj Evolve - Entire List - Seg A - from PP Tech Solutions
List ID: 5547
"""

# n.get_npi_list('data', 5547)

"""
GET ALL NPI LISTS
"""

# n.get_all_npi_lists(561939)

"""
create_npi_list method:

CREATE NPI list for PP Tech Solutions. 
Acct ID - 561939
"""


n.create_npi_list(561939)


# testing out the df process
new_lists = []

df = pd.read_csv('./data/test/npi_test_single.csv')[['TargetListID', 'NPI_ID']]
#df = pd.read_csv('./data/test/npi_test.csv')[['TargetListID', 'NPI_ID']]
df = df.dropna()

for target in df['TargetListID'].unique():
    single_list = df[df['TargetListID'] == target].reset_index(drop=True)
    single_list = single_list['NPI_ID'].apply(lambda x: str(int(x))).to_list()

    final_list = dict(name=target, npis=single_list)
    new_lists.append(final_list)

    # print(f'final_list is: \n {json.dumps(final_list, indent=2)}')
    # print(f'new_lists holds: \n {json.dumps(new_lists, indent=2)}')


print(f'We have detected {len(new_lists)} list/s to be created this could take {len(new_lists)} mins or more to upload \n')

try:
    for i, v in enumerate(new_lists):
        r = requests.post('https://httpbin.org/post', json=json.dumps(v))
        r.raise_for_status()

        if r.status_code == requests.codes.ok:
            progress_bar()
            print(f'List #{i + 1} uploaded 👍')

except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

