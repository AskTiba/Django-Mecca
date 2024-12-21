## In the terminal, you can use the following tools to explore data structures:

    ## type() – Identify the type.
    ## dir() – List available methods and attributes.
    ## help() – Get detailed documentation.
    ## print() – View the contents.
    ## len() – Get the number of elements.
    ## sys.getsizeof() – Get memory size.
    ## pprint – Print structures nicely.


```Python
#* authenticate to X.com
#! 1) use the login credentials. 2) use cookies.
client = Client(language='en-US')
client.login(auth_info_1=username, auth_info_2=email, password=password)
client.save_cookies('cookies.json')
```