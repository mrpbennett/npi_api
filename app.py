"""
CLI application so a user can run the CLI in the cmd line.
"""
from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from simple_chalk import chalk
from npi_class import NPIListApi

print(chalk.blue('Welcome to our LIFE API for dealing with NPI lists.'))

# Initial user questions to generate user credentials.
user_id_questions = [
    {
        'type': 'input',
        'name': 'account_id',
        'message': 'Enter your ACCOUNT NAME',
    },
    {
        'type': 'password',
        'message': 'Enter your account PASSWORD',
        'name': 'password'
    }
]

user_id_answers = prompt(user_id_questions)

# Store the username and password within the class instance
n = NPIListApi(user_id_answers.get('account_id'), user_id_answers.get('password'))

# storing length of user credentials
len_of_account_id = len(user_id_answers.get('account_id'))
len_of_password = len(user_id_answers.get('password'))

if len_of_account_id and len_of_password >= 6:

    # This generates a list of choices for the user
    user_task_questions = [
        {
            'type': 'list',
            'name': 'theme',
            'message': 'What task would you like to complete?',
            'choices': [
                'GET an NPI list',
                'GET ALL NPIs for account',
                'CREATE an NPI list',
                'REPLACE NPIs within a list',
                'ADD NPIs to a list',
                'DELETE NPIs from a list'

            ]
        },
    ]

    user_task_answers = prompt(user_task_questions)

    if user_task_answers.get('theme') == "GET an NPI list":

        get_npi_list_questions = [
            {
                'type': 'input',
                'name': 'list_id',
                'message': 'Please provide the LIST ID you wish to generate'
            }
        ]

        get_npi_list_answers = prompt(get_npi_list_questions)
        n.get_npi_list(get_npi_list_answers.get('list_id'))

    if user_task_answers.get('theme') == 'GET ALL NPIs for account':

        get_all_npi_questions = [
            {
                'type': 'input',
                'name': 'account_id',
                'message': 'Please provide the account ID you wish to retrieve all lists from.'
            }
        ]

        get_all_npi_answers = prompt(get_all_npi_questions)
        n.get_all_npi_lists(get_all_npi_answers.get('account_id'))

    if user_task_answers.get('theme') == "CREATE an NPI list":

        get_create_npi_questions = [
            {
                'type': 'input',
                'name': 'account_id',
                'message': 'Please provide the account ID you wish to upload the your new list too.'
            }
        ]

        get_create_npi_answers = prompt(get_create_npi_questions)
        n.create_npi_list(get_create_npi_answers.get('account_id'))

    if user_task_answers.get('theme') == "REPLACE NPIs within a list":

        get_replace_npi_list_questions = [
            {
                'type': 'input',
                'name': 'list_id',
                'message': 'Please provide the LIST ID of the list you wish to REPLACE NPIs on'
            }
        ]

        get_replace_npi_list_answers = prompt(get_replace_npi_list_questions)
        n.get_npi_list(get_replace_npi_list_answers.get('list_id'))

    if user_task_answers.get('theme') == "ADD NPIs to a list":

        get_add_npi_list_questions = [
            {
                'type': 'input',
                'name': 'list_id',
                'message': 'Please provide the LIST ID you wish to ADD NPIs too'
            }
        ]

        get_add_npi_list_answers = prompt(get_add_npi_list_questions)
        n.get_npi_list(get_add_npi_list_answers.get('list_id'))

    if user_task_answers.get('theme') == "DELETE NPIs from a list":

        get_delete_npi_list_questions = [
            {
                'type': 'input',
                'name': 'list_id',
                'message': 'Please provide the LIST ID you wish to DELETE NPIs from'
            }
        ]

        get_delete_npi_list_answers = prompt(get_delete_npi_list_questions)
        n.get_npi_list(get_delete_npi_list_answers.get('list_id'))

