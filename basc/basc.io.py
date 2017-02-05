import requests
import urllib
from figo import FigoSession
from PageResponses import Page1Response
from PageResponses import Page2Response
from PageResponses import Page3Response
from lxml import html
from requests.auth import HTTPBasicAuth
from config import figoSettings
from AccessToken import AccessToken


class FigoConnection(object):
    pass

    AUTH_BASE_URL = 'https://api.figo.me/auth'

    HEADERS = {'content-type': 'application/x-www-form-urlencoded',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.8,de;q=0.6'}

    @classmethod
    def request_page_one(cls):
        payload = {'response_type': 'code', 'client_id': figoSettings['figo']['clientId'],
                   'state': 'xqD6gjrygsAlT0uC'}

        response = requests.get(cls.AUTH_BASE_URL + "/code", params=payload)
        tree = html.fromstring(response.content)

        return Page1Response(tree.xpath('//input[@name="id"]/@value'), tree.xpath('//input[@name="step"]/@value'))

    @classmethod
    def request_page_two(cls, page1response):
        payload = {'username': figoSettings['figo']['username'], 'password': figoSettings['figo']['password'],
                   'id': page1response.get_response_id(), 'step': page1response.get_step()}

        response = requests.post(cls.AUTH_BASE_URL + "/login", data=urllib.urlencode(payload),
                                 headers=cls.HEADERS)
        tree = html.fromstring(response.content)

        return Page2Response(tree.xpath('//input[@name="id"]/@value'), tree.xpath('//input[@name="step"]/@value'),
                             tree.xpath('//input[@type="checkbox"]/@id'))

    @classmethod
    def request_page_three(cls, page2response):
        payload = {'A1238764.4': '1', 'A1238764.5': '1', 'id': page2response.get_response_id(),
                   'step': page2response.get_step()}

        response = requests.post(cls.AUTH_BASE_URL + "/login", data=urllib.urlencode(payload),
                                 headers=FigoConnection.HEADERS, allow_redirects=False)

        return Page3Response(response.headers['Location'].split("=")[2])

    @classmethod
    def request_page_four(cls, page3response):
        payload = {'grant_type': 'authorization_code', 'code': page3response.get_code()}

        response = requests.post("https://api.figo.me/auth/token", data=urllib.urlencode(payload),
                                 headers=FigoConnection.HEADERS,
                                 auth=HTTPBasicAuth(figoSettings['figo']['clientId'],
                                                    figoSettings['figo']['secret']))

        return AccessToken(response.json()["access_token"])

    @staticmethod
    def query_api(account_id, token):
        FigoConnection.HEADERS.update({'Authorization': 'Bearer ' + token})
        response = requests.get("https://api.figo.me/rest/accounts/" + account_id,data=None,headers=FigoConnection.HEADERS)

        if response.status_code != 401:
            account = response.json()
            print account['balance']['balance']


if __name__ == '__main__':
    fc = FigoConnection()
    p1r = fc.request_page_one()
    p2r = fc.request_page_two(p1r)
    p3r = fc.request_page_three(p2r)
    at = fc.request_page_four(p3r)
    fc.query_api('A1238764.4', at.get_access_token())

