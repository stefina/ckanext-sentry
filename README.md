[![Tests](https://github.com/stefina/ckanext-sentry/workflows/Tests/badge.svg?branch=main)](https://github.com/stefina/ckanext-sentry/actions)

# ckanext-sentry

This plugin adds sentry as middleware using sentry_sdk to log directly to Sentry.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible? |
|-----------------|-------------|
| 2.9             | not tested  |
| 2.10            | not tested  |
| 2.11            | yes         |


## Installation

To install ckanext-sentry:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/stefina/ckanext-sentry.git
    cd ckanext-sentry
    pip install -e .
	pip install -r requirements.txt

3. Add `sentry` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

The default configuration will send all logs with the level ERROR to Sentry. All you have to configure to get started is the Sentry-DSN:

	# The project-specific DSN-URL-String. See here, how to find it: https://docs.sentry.io/product/sentry-basics/dsn-explainer/#where-to-find-your-dsn
	# (mandatory, default: "").
	ckanext.sentry.dsn = https://bdda2dd00b2bb8296f4da0767b8a7adc@o198669.ingest.us.sentry.io/4509909612298240

You can deactivate the creation of the sentry-middleware using this configuration:

    # Enable/disable logging to sentry:
	# (optional, default: True).
	ckanext.sentry.enable_logging = False

Configure global error logging (useful for error-reporting in sentry):
    
    # Configure global error logging to log all messages of a log-level to Sentry.
    # (optional, default: False).
    ckanext.sentry.global_error_logging = True

    # Configure the log-level of global error logging to log all messages to Sentry.
    # (optional, default: ERROR).
    ckanext.sentry.global_error_logging.log_level = WARNING

Configure loggers for fine-granular logging (useful for more advanced, fine-granular logging and debugging):

    # Configure loggers, separated with spaces, for sentry.
    # (optional, default: "" ckan ckanext sentry.errors).
	ckanext.sentry.loggers = ckan ckanext
    
    # Control whether a logger passes its log records up the hierarchy. Setting it to `False` gives you a fine-grained logging control. Setting this to `True` can create duplicates:
	# (optional, default: False).
	ckanext.sentry.propagate = True

    # Configure log_level for sentry:
	# (optional, default: WARNING).
	ckanext.sentry.log_level = WARNING

Example configuration for sending all logs to Sentry:

    # If you want all log-entries be sent to Sentry and configure all the resulting actions in Sentry itself, it is recommended to configure it like this:
	ckanext.sentry.loggers = ckan ckanext
    # Adding `""` will also include the root-logger.
    ckanext.sentry.loggers = "" ckan ckanext
    ckanext.sentry.log_level = WARNING

Example configuration for sending logs to Sentry from specific plugins only for debugging: 

    # If you want to use Sentry to debug specific plugins only, you can specify the plugins like this:
    ckanext.sentry.loggers = ckanext.dcat ckanext.harvest ckanext.my_custom_harvest_plugin.my_custom_harvester
    # Also set propagation to `False` to allow fine-grained logging without duplicates from parent-loggers.
    ckanext.sentry.propagate = False
    ckanext.sentry.log_level = DEBUG


## Developer installation

To install ckanext-sentry for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/stefina/ckanext-sentry.git
    cd ckanext-sentry
    pip install -e .
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-sentry

If ckanext-sentry should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `pyproject.toml` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python -m build && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
