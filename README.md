# NPI List API CLI

I have built a CLI to handle the uses of our LIFE API, allowing users to do the following via the methods:

1. [`get_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L46) allows users to retrieve a list of all NPI's that are in a NPI List
2. [`get_all_npi_lists()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L75) allows users to get a list of all NPI lists associated with an account
3. [`create_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L108) allows users to create a new NPI list and add NPIs to the new list
4. [`replace_npi_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L149) allows users to replace all NPI's in one list
5. [`add_npi_to_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L168) allows users to add NPIs to an existing NPI list
6. [`delete_npi_from_list()`](https://github.com/mrpbennett/npi_api/blob/94764b6cf3e19c20e2d58db7fb5b7852927ded79/npi_class.py#L188) allows users to delete NPIs from one list

There is also a `@staticmethod` that prevents from users overloading the API when it comes to creating multiple lists.

```python
@staticmethod
def progress_bar():
    with Bar(f"Uploading!", fill="🟪", max=61, suffix='%(percent)d%%') as bar:
        for _ in range(61):
            time.sleep(1)
            bar.next()
```

Each method sits in a class called `NPIListApi` this holds the brains of the application.

The CLI is powered by `PyInquirer` and `simple_chalk` to make it look user-friendly.

Before all the above starts we need to get our authentication token and establish the connection. We do this by using the following method in the `NPIListApi` class.

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

This uses the awesome library called [Authlib](https://docs.authlib.org/en/latest/)
