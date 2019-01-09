# Item Catalog

The application displays a list of sports-related items in a variety of formats. Users may view a list of all items, recently created items, or a number of items that match certain sport or category. Users may also view individual items and their descriptions. Users may log in with GitHub to create their own items, which may be updated or deleted. Items may only be updated or deleted by their creators, and items that are "private" may only be viewed by their creators.

The application also implements a number of JSON endpoints, including all items, recent items, individual items, and items for a specific sport or category. JSON endpoints do not include items that are set to "private" by their creators.

### Notes

If you would like to see this app in action, or if you would like to deploy the app for yourself, please see the **Deployment** section below.

If you would like to run the app locally on your computer, follow the instructions listed in the **Dependencies** and **Usage** sections below.

## Deployment

This application has been deployed on Heroku, [here](https://item-catalog-demo.herokuapp.com/).

The application is deployment-ready via Heroku, with the exception of setting environment variables. If you would like to deploy this application on Heroku, please see [this tutorial](https://devcenter.heroku.com/articles/getting-started-with-python) for deploying the application. As you follow the tutorial, you will need to install Heroku's PostgreSQL addon, then use `$ heroku config` to view your environment variables. The following environment variables must be set:

* IC_SECRET
* IC_DATABASE
* IC_CLIENT_ID
* IC_CLIENT_SECRET

Use [this documentation](https://devcenter.heroku.com/articles/config-vars) to understand how to set environment variables for your Heroku app. Follow the instructions in **Dependencies** (below) under _Secret Key and Database URI_ to obtain a value for "IC_SECRET", and under _GitHub OAuth App_ to obtain values for "IC_CLIENT_ID" and "IC_CLIENT_SECRET". To obtain a value for "IC_DATABASE", however, you must use the value of "DATABASE_URL".

After you have set all four environment variables, the app should be fully functional.

## Dependencies

You will need access to a shell terminal (I am using [GitBash](https://git-scm.com/downloads) for Windows). You will also need to install the latest version of [Python 3](https://www.python.org/downloads/), which must be Python 3.6 or later. This app is incompatible with Python 2 and Python 3.5 or older. The deployed version of this application uses Python 3.7.1.

Once you have a shell terminal and Python 3 installed, you can start by cloning the repository:

```
$ git clone https://github.com/davidhammaker/Item_Catalog.git
```

Navigate into the repository to complete _Installation Requirements_ below.

### Installation Requirements

It is recommended that you install all Python packages in a virtual environment. Documentation for setting up a virtual environment using `venv` may be found [here](https://docs.python.org/3/library/venv.html).

After creating and activating a new virtual environment, run the following command to install the required packages:

```
$ pip install -r requirements.txt
```

* Note: If your default version of Python is not Python 3, you will have to use `pip3` instead of `pip`.

### Secret Key and Database URI

Both the application secret key (for forms) and the database URI have been set to environment variables for optimum security. Prior to running the application, you must set up these environment variables.

* Skipping this step: If you are not concerned about security, you can edit 'item_catalog/config.py' and replace the environment variables with strings of your choice:
```
IC_SECRET = 'secret'
IC_DATABASE = 'sqlite:///example.db'
```

If you would like to learn how to set up environment variables, here are a few brief videos that explain the process for [Windows](https://www.youtube.com/watch?v=IolxqkL7cD8) and [Mac and Linux](https://www.youtube.com/watch?v=5iWhQWVXosU). (Note: I was only successful when I followed the "Mac and Linux" tutorial using GitBash for Windows.) The first two environment variables must be named "IC_SECRET" and "IC_DATABASE". Follow these steps to obtain values for each:

* Obtain a value for "IC_SECRET" by opening a Python REPL and entering the following:
```
>>> import secrets
>>> secrets.token_hex(16)
```
The result should be a long string of random characters. Set your environment variable to this result.

* The value you choose for "IC_DATABASE" is somewhat arbitrary. Just make sure you prefix your value with something like `sqlite:///`, and add the `.db` file extension. For example, `sqlite:///example.db` would work.

### GitHub OAuth App

For 3rd party OAuth provision to function properly, you must create an OAuth App in GitHub. You may create an app [here](https://github.com/settings/applications/new). Set "Homepage URL" to "http://localhost:5000", and "Authorization callback URL" to "http://localhost:5000/login/github/authorized". (_Note_: If you are deploying the application to Heroku, or any other host, use the home-page URL for your deployment instead of "http://localhost:5000".) The other fields maybe filled in however you want. Register your app and find values for "Client ID" and "Client Secret". Create environment variables with these values, named "IC_CLIENT_ID" and "IC_CLIENT_SECRET" respectively.

* If setting the environment variables is unsuccessful, you may insert the values directly into your code for demonstration purposes only.
```
blueprint = make_github_blueprint(
    client_id="insert-your-clinet-id",
    client_secret="insert-your-client-secret"
)
```
Note that this is an insecure means of incorporating these values in your code.

### Other Requirements

This application uses Flask-Dance to implement 3rd party OAuth provision. By default, Flask-Dance requires HTTPS, or the application will not run. This requirement may be suppressed by running the following:

```
$ export OAUTHLIB_INSECURE_TRANSPORT=1
```

* Note that this is an insecure means of running the application and should only be used when testing the application on a local device.

## Usage

_Remember that you must set "OAUTHLIB INSECURE TRANSPORT" prior to running the application locally. See "Dependencies" for more information._

When running the application for the first time, you have a few different options for how you would like to set up the application. You may set up the application with an empty database (with no items in the catalog), or you may fill in the database with pre-made items at the time of its creation. If you set up the application with an empty database, you can still fill the database with the pre-made items later.

In all of the following cases, if Python 3 is not the default version of Python on your computer, substitute `python3` for `python` in all of your shell commands.

### Set up the application with an empty database

Make sure your virtual environment is active, then run `$ python run.py --setup`. This will set up your database with empty tables so that items may be added to the catalog manually. The application will start automatically. Open an internet browser and navigate to 'localhost:5000' to use the application.

If you close the application in your terminal, you may start it up again by running `$ python run.py`.

### Set up the application with a pre-filled database

Make sure your virtual environment is active, then run `$ python fill.py --setup`. This will set up your database with an example user and many new items.

To start the application, run `$ python run.py`.

### Fill a pre-existing database with data

Make sure your virtual environment is active, then run `$ python fill.py`. If there are no conflicts between the new data and any pre-existing data in the database, the database should fill with an example user and new items.

Again, you may start the application with `$ python run.py`.


## Trivia

This application was originally my submission for the "Item Catalog" project in Udacity's Full Stack Development Nanodegree program.


## Copyright

© David J. Hammaker 2018-2019
