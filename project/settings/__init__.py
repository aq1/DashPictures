from project.settings.base_settings import *
from project.settings.local_settings import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn="https://24ce410c546b4ef9a7a76e81c322e66c@sentry.io/1867013",
        integrations=[DjangoIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
