import os

import pytest
from dotenv import load_dotenv
from selene import browser
from clients.spends_client import SpendsHttpClient


@pytest.fixture(scope='session')
def envs():
    load_dotenv()


@pytest.fixture(scope='session')
def frontend_url(envs):
    return os.getenv('FRONTEND_URL')


@pytest.fixture(scope='session')
def gateway_url(envs):
    return os.getenv('GATEWAY_URL')


@pytest.fixture(scope='session')
def app_user(envs):
    return os.getenv('TEST_USERNAME'), os.getenv('TEST_PASSWORD')


@pytest.fixture(scope='session')
def auth(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element("a[href*='redirect']").click()
    browser.element("input[name='username']").set_value(username)
    browser.element("input[name='password']").set_value(password)
    browser.element("button[type='submit']").click()

    return browser.driver.execute_script('return window.sessionStorage.getItem("id_token")')


@pytest.fixture(scope='session')
def spends_client(gateway_url, auth) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, auth)

@pytest.fixture(params=[])
def spends(request, spends_client):
    test_spend = spends_client.add_spends(request.param)
    yield test_spend
    all_spends = spends_client.get_spends()
    if test_spend["id"] in [spend["id"] for spend in all_spends]:
        spends_client.remove_spends([test_spend["id"]])


@pytest.fixture()
def main_page(auth, frontend_url):
    browser.open(frontend_url)



@pytest.fixture(params=[])
def category(request, spends_client):
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category['category'] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)
    return category_name
