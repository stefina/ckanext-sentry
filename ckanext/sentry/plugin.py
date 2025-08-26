import logging
import sentry_sdk
from sentry_sdk.integrations.logging import EventHandler, BreadcrumbHandler
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

log = logging.getLogger(__name__)





class SentryPlugin(plugins.SingletonPlugin):
    """A simple plugin that adds the Sentry middleware to CKAN"""

    plugins.implements(plugins.IMiddleware, inherit=True)

    def make_middleware(self, app, config):
        CKAN_SENTRY_CONFIGURE_LOGGING = toolkit.asbool(toolkit.config.get("ckanext.sentry.configure_logging", False))
        if CKAN_SENTRY_CONFIGURE_LOGGING:
            return self.make_error_log_middleware(app, config)
        else:
            return app

    def make_error_log_middleware(self, app, config):
        CKAN_SENTRY_DSN = toolkit.config.get("ckanext.sentry.dsn", None)
        sentry_sdk.init(
            dsn=CKAN_SENTRY_DSN,
            release="1.3.0",
            send_default_pii=True,
        )
        self._configure_logging()

        log.debug('Adding Sentry middleware...')
        sentry_wrapped = SentryWsgiMiddleware(app)
        return sentry_wrapped

    def _configure_logging(self):
        """
        Configure the Sentry log handler to the specified level
        """
        CKAN_SENTRY_LOG_LEVEL = toolkit.config.get("ckanext.sentry.log_level", logging.INFO)
        loggers = ["", "ckan", "ckanext", "sentry.errors"]
        for name in loggers:
            logger = logging.getLogger(name)
            logger.setLevel(CKAN_SENTRY_LOG_LEVEL)
            logger.addHandler(BreadcrumbHandler(level=CKAN_SENTRY_LOG_LEVEL))
            logger.addHandler(EventHandler(level=logging.ERROR))

        log.debug("Setting up Sentry logger with level {0}".format(CKAN_SENTRY_LOG_LEVEL))