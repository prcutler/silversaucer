import os

# Discogs
discogs_user_token = ""
discogs_user_agent = "SilverSaucer/0.1"

# Only use this if you cannot use environment variables (which are recommended)
discogs_key = ""
discogs_secret = ""
discogs_oauth_token_secret = ""
discogs_oauth_verifier = ""
discogs_oauth_token = ""

discogs_url = "https://api.discogs.com/"

discogs_user = "prcutler"

username = ""
password = ""

# Login cookie signing key. Required in production; prefer the
# SILVERSAUCER_SECRET_KEY environment variable. Generate one with:
#   python -c "import secrets; print(secrets.token_hex(32))"
secret_key = ""

# Only send the login cookie over HTTPS (or set SILVERSAUCER_SECURE_COOKIES=1).
# Leave False for local development on http://127.0.0.1.
secure_cookies = False
