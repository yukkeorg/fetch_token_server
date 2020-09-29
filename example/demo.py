import os
import webbrowser
import logging

from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

from . import serve_fetch_token_server

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"


def main():
    #####
    # Setup
    #####

    # Set up logger configuration.
    logging.basicConfig(level='DEBUG')

    # Support a insecure redirect connection (e.g. HTTP) in OAuthLib.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # loading the credential informations from .env file.
    load_dotenv()

    client_id = os.environ.get("GITHUB_CLIENT_ID")
    if client_id is None:
        logging.error("[!!] GITHUB_CLIENT_ID is not set.")
        return 1

    client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
    if client_secret is None:
        logging.error("[!!] GITHUB_CLIENT_SECRET is not set.")
        return 2

    #####
    # Authorize with OAuth2
    #####
    github_session = OAuth2Session(client_id)

    authorization_url, state = github_session.authorization_url(GITHUB_AUTH_URL)
    logging.debug(f"Authoraization URL : {authorization_url}")

    webbrowser.open(authorization_url)

    redirect_response = serve_fetch_token_server()
    logging.debug(f"Redirect URL: {redirect_response}")

    github_session.fetch_token(GITHUB_TOKEN_URL,
                               client_secret=client_secret,
                               authorization_response=redirect_response)

    #####
    # Use API with OAuth2
    #####
    r = github_session.get("https://api.github.com/user")
    print(r.content)


if __name__ == "__main__":
    main()
