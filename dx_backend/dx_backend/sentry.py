import os
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

logger = logging.getLogger(__name__)

SENTRY_DSN = os.getenv("SENTRY_DSN")
if not SENTRY_DSN:
    raise ImportError(
        "SENTRY_DSN environment variable is not set. Please set it to your Sentry DSN."
    )


def before_send(event, hint):
    """
    Custom handler for events before they're sent to Sentry.
    Particularly focused on handling 500 errors properly.
    """
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        logger.error(f"Sending error to Sentry: {exc_type.__name__}: {exc_value}")

        # Add additional context for 500 errors
        if event.get('level') == 'error' or event.get('exception', {}).get('values', [{}])[0].get('type') in [
            'Internal Server Error', 'ServerError', 'HTTPException'
        ]:
            # Add custom tags for better filtering
            if 'tags' not in event:
                event['tags'] = {}
            event['tags']['error_type'] = '500_server_error'

            # Add additional context that might be helpful
            if 'request' in event and event['request']:
                # Log request details for server errors
                request_data = event['request']
                logger.error(f"500 error on URL: {request_data.get('url', 'unknown')}")
                logger.error(f"Method: {request_data.get('method', 'unknown')}")

    return event


# Initialize Sentry SDK with custom configuration
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[
        DjangoIntegration(),
        LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        ),
    ],
    # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring
    # We recommend adjusting this value in production
    traces_sample_rate=0.1,

    # Enable performance monitoring
    enable_tracing=True,

    # Configure the before_send handler for custom error processing
    before_send=before_send,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",

    # Set a uniform sample rate for all users
    # If you want to implement sampling based on user or other criteria,
    # use the before_send callback for more complex cases
    sample_rate=1.0,

    # Disable auto session tracking to reduce noise
    auto_session_tracking=False,
)
