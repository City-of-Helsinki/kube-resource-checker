import os
import requests

def getSession() :
    auth_domain=os.environ.get('DOMAIN')
    cookie_oauth2_proxy=os.environ.get('COOKIE_OAUTH_PROXY')
    session = requests.Session()
    session.cookies.set("_oauth2_proxy", cookie_oauth2_proxy, domain=auth_domain)
    return session