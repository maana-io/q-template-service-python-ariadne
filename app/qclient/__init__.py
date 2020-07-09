import os
import logging
import requests
import json
import time

from graphqlclient import GraphQLClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.auth.env'))


class QClientError(Exception):
    def __init__(self, message):
        self.message = message


class QClient:
    def __init__(
            self,
            endpoint,
            auth_provider=os.getenv('AUTH_PROVIDER'),
            auth_domain=os.getenv('AUTH_DOMAIN'),
            auth_client_id=os.getenv('AUTH_CLIENT_ID'),
            auth_secret=os.getenv('AUTH_SECRET'),
            auth_identifier=os.getenv('AUTH_IDENTIFIER'),
            require_auth=True):
        if not endpoint:
            raise QClientError('Client endpoint is not provided')

        self.require_auth = require_auth
        self.endpoint = endpoint

        if require_auth:
            self.access_token = None
            self.refresh_token = None
            self.access_token_expiration_ts = 0
            self.refresh_token_expiration_ts = 0

            if (auth_provider == 'keycloak'):
                self.auth_url = f'{auth_domain}/auth/realms/{auth_identifier}/protocol/openid-connect/token'
            elif (auth_provider == 'auth0'):
                self.auth_url = f'https://{auth_domain}/oauth/token'
            else:
                raise QClientError(
                    'Only Keycloak and Auth0 are supported at the moment')
            self.client_id = auth_client_id
            self.client_secret = auth_secret
            self.auth_identifier = auth_identifier
            self._authenticate()
        else:
            logging.info(
                f'Client for endpoint {endpoint} is created without authentication')
        self.underlying = GraphQLClient(endpoint)

    def _authenticate(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'audience': self.auth_identifier
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        r = requests.post(self.auth_url, data=payload, headers=headers)
        response_data = r.json()
        self.access_token = response_data['access_token']
        self.access_token_expiration_ts = int(
            time.time() + response_data['expires_in'] * 0.9)
        access_token_expiration_str = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(self.access_token_expiration_ts))
        # If refresh token is configured (on by default in keycloak, requires extra configuration in Auth0), use it
        # Otherwise, fall back to regular authentication flow
        if 'refresh_token' in response_data:
            self.refresh_token = response_data['refresh_token']
            self.refresh_token_expiration_ts = int(
                time.time() + response_data['refresh_expires_in'] * 0.9)
            refresh_token_expiration_str = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(self.refresh_token_expiration_ts))
            logging.info(
                f'Authenticated with {self.auth_url}, access token expires at {access_token_expiration_str}, refresh token expires at {refresh_token_expiration_str}')
        else:
            logging.info(
                f'Authenticated with {self.auth_url}, access token expires at {access_token_expiration_str}, refresh token is received')

    def _refresh(self):
        if not self.refresh_token or int(time.time()) > self.refresh_token_expiration_ts:
            self._authenticate()
            return

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        r = requests.post(self.auth_url, data=payload, headers=headers)
        response_data = r.json()
        self.access_token = response_data['access_token']
        self.access_token_expiration_ts = int(
            time.time() + response_data['expires_in'] * 0.9)
        access_token_expiration_str = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(self.access_token_expiration_ts))
        logging.info(
            f'Refreshed access token, it expires at {access_token_expiration_str}')

    def _get_token(self):
        if not self.access_token:
            self._authenticate()
            return self.access_token

        if int(time.time()) > self.access_token_expiration_ts:
            self._refresh()
            return self.access_token

        return self.access_token

    def execute(self, query, variables=None):
        if self.require_auth:
            token = self._get_token()
            self.underlying.inject_token(f'Bearer {token}')
            return self.underlying.execute(query, variables)
        else:
            self.underlying.execute(query, variables)
