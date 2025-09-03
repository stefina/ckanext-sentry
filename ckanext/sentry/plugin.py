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
        CKAN_SENTRY_LOG_LEVEL_NAME = self._parse_log_level_name("ckanext.sentry.log_level")
        CKAN_SENTRY_LOG_LEVEL_INT = self._parse_log_level_int("ckanext.sentry.log_level")
        CKAN_SENTRY_LOGGERS = toolkit.config.get("ckanext.sentry.loggers", None)
        CKAN_SENTRY_PROPAGATE = toolkit.asbool(toolkit.config.get("ckanext.sentry.propagate", False))

        if CKAN_SENTRY_LOGGERS:
            loggers = CKAN_SENTRY_LOGGERS.split()
        else:
            loggers = ["", "ckan", "ckanext", "sentry.errors"]
        for name in loggers:
            logger = logging.getLogger(name)
            logger.propagate = CKAN_SENTRY_PROPAGATE
            logger.addHandler(BreadcrumbHandler(level=CKAN_SENTRY_LOG_LEVEL_INT))
            logger.addHandler(EventHandler(level=CKAN_SENTRY_LOG_LEVEL_INT))

        log.debug("Setting up Sentry logger with level {0}".format(CKAN_SENTRY_LOG_LEVEL_NAME))

    def _parse_log_level_name(self, conf):
        raw_level = self._parse_log_level_int(conf)
        name = str(raw_level).strip().upper()
        return logging.getLevelName(name)

    def _parse_log_level_int(self, conf):
        return toolkit.config.get(conf, logging.WARNING)
