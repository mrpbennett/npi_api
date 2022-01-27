# NPI List API CLI

I have built a CLI to handle the uses of our LIFE API, allowing users to do the following via the methods:

1. [`get_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L46) allows users to retrieve a list of all NPI's that are in a NPI List
2. [`get_all_npi_lists()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L75) allows users to get a list of all NPI lists associated with an account
3. [`create_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L108) allows users to create a new NPI list and add NPIs to the new list
4. [`replace_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L165) allows users to replace all NPI's in one list
5. [`add_npi_to_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L215) allows users to add NPIs to an existing NPI list
6. [`delete_npi_from_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L261) allows users to delete NPIs from one list

There is also a `@staticmethod` that prevents from users overloading the API when it comes to creating multiple lists.

```python
@staticmethod
def progress_bar():
    with Bar(f"Please wait", fill="🟪", max=61, suffix='%(percent)d%%') as bar:
        for _ in range(61):
            time.sleep(1)
            bar.next()
```

The output from `progress_bar()` should look as follows:

<img width="676" alt="Screenshot 2022-01-27 at 13 52 47" src="https://user-images.githubusercontent.com/1844080/151379325-b248e8a7-9e34-4d7f-8c3a-f4d10dc14345.png">

My thought process behind this was that I need the progress bar to last 1 minute, as I have used this to prevent an overload of an API. So I used `max` and gave it an int of `61` with a `range(61)` then gave the for loop a `time.sleep(1)` of one 1 second. The loop will last for 61 seconds (_just incase it doesn't allow anything equal to 60 seconds_)', due to the `range(61)`, the `max` value allows the `suffix` to display the correct percentage.


### The Class 🧠

Without this class the CLI would be useless, each method sits in a under a class called `NPIListApi` this holds the brains of the application. Each method preforms a single task of the API, these are mentioned above but as follows:

1. [`get_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L46) 
2. [`get_all_npi_lists()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L75) 
3. [`create_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L108) 
4. [`replace_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L165) 
5. [`add_npi_to_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L215) 
6. [`delete_npi_from_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L261)

To allow our users to use this CLI first the application has to grab an authentication token and establish the connection. We do this by using the [`establish_connection()`](https://github.com/mrpbennett/npi_api/blob/3b911f3c065f791940be7c29f0b0c0a6ca66a5d3/npi_class.py#L29) method in the `NPIListApi` class. The authentication is handled by a library called [Authlib](https://docs.authlib.org/en/latest/)

```python
def establish_connection(self):
    # Fetch an access token from the provider.
    client = OAuth2Session(self.client_id, self.client_secret)
    token = client.fetch_token(self.auth_url, authorization_response=self.auth_url,
                               username=self.username, password=self.password, grant_type='password')

    # establish a new client with the token we got above
    client = OAuth2Session(self.client_id, self.client_secret, token=token)

    return client
```

### The CLI 💻

This is powered by `PyInquirer` and `simple_chalk` to make it look user-friendly. The whole of the CLI interface is in [app.py](https://github.com/mrpbennett/npi_api/blob/master/app.py) once the user has been prompted to enter their credentials. A selection of choices are presented to them via this prompt

```python
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
```

Once a user has selected an option to complete, the CLI will then move on to another selection of questions. These questions will help the user complete the request. For example if the user selected `"CREATE an NPI list"` the below would fire off. Allowing the user to input their `account_id` which would run the 
[`create_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L108) method.

```python
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
```

More to come ...