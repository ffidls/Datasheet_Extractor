"""Resources for making Nexar requests."""
import requests
import base64
import json
import time
from typing import Dict


NEXAR_URL = "https://api.nexar.com/graphql"
PROD_TOKEN_URL = "https://identity.nexar.com/connect/token"


def get_token(client_id, client_secret):
    """Return the Nexar token from the client_id and client_secret provided."""

    if not client_id or not client_secret:
        raise Exception("client_id and/or client_secret are empty")

    token = {}
    try:
        token = requests.post(
            url=PROD_TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            },
            allow_redirects=False,
        ).json()

    except Exception:
        raise

    return token


def decodeJWT(token):
    return json.loads(
        (base64.urlsafe_b64decode(token.split(".")[1] + "==")).decode("utf-8"))


class NexarClient:
    def __init__(self, id, secret) -> None:
        self.id = id
        self.secret = secret
        self.s = requests.session()
        self.s.keep_alive = False

        self.token = get_token(id, secret)
        self.s.headers.update({"token": self.token.get('access_token')})
        self.exp = decodeJWT(self.token.get('access_token')).get('exp')

    def check_exp(self):
        if self.exp < time.time() + 300:
            self.token = get_token(self.id, self.secret)
            self.s.headers.update({"token": self.token.get('access_token')})
            self.exp = decodeJWT(self.token.get('access_token')).get('exp')

    def get_query(self, query: str, variables: Dict) -> dict:
        """Return Nexar response for the query."""
        try:
            self.check_exp()
            r = self.s.post(
                NEXAR_URL,
                json={"query": query, "variables": variables},
            )

        except Exception as e:
            print(e)
            raise Exception("Error while getting Nexar response")

        response = r.json()
        if "errors" in response:
            for error in response["errors"]: print(error["message"])
            raise SystemExit

        return response["data"]


QUERY_MPN = '''
query Search($mpn: String!) {
    supSearchMpn(q: $mpn, limit: 2) {
      results {
        part {
          mpn
          shortDescription
          manufacturer {
            name
          }
          specs {
            attribute {
              shortname
            }
            value
          }
        }
      }
    }
  }
'''


def getLifecycleStatus(specs):
    if specs:
        lifecycleSpec = [i for (i) in specs if i.get('attribute', {}).get('shortname') == 'lifecyclestatus']
        if len(lifecycleSpec) > 0:
            return lifecycleSpec[0].get('value', {})
    return ''


def get_inf_PN(pn_lst, test_fl=False):
    clientId = '6af7a788-4f5a-4a8a-ba12-6c8e0dbe00f7'
    clientSecret = '13fd9ef2-9877-4bda-87f8-06ad951547f3'
    nexar = NexarClient(clientId, clientSecret)
    all_inf = []
    s = 0

    for pn in pn_lst:
        print(pn)
        variables = {
            'mpn': pn
        }
        try:
            results = nexar.get_query(QUERY_MPN, variables)

            if results:
                for it in results.get("supSearchMpn", {}).get("results", {}):
                    a = ''
                    a += f'MPN: {it.get("part",{}).get("mpn")}\n'
                    a += f'Description: {it.get("part",{}).get("shortDescription")}\n'
                    a += f'Manufacturer: {it.get("part",{}).get("manufacturer",{}).get("name")}\n'
                    a += f'Lifecycle Status: {getLifecycleStatus(it.get("part",{}).get("specs",{}))}\n'
                    a += '\n'
                    all_inf.append(a)
                    s += 1

        except Exception:
            if test_fl and s == 0:
                return None, s
            continue

    all_inf = set(all_inf)
    return all_inf, s

