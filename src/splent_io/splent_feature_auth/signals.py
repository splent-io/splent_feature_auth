"""
Signals emitted by the auth feature.

Other features can listen to these signals to react to auth events
without importing auth's internal modules.
"""

from splent_framework.signals.signal_utils import define_signal

user_registered = define_signal("user-registered", "splent_feature_auth")
