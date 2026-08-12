import os

import pytest
from dotenv import load_dotenv
from selene import browser
from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from models.config import Envs


@pytest.fixture(scope='session')
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv('FRONTEND_URL'),
        gateway_url=os.getenv('GATEWAY_URL'),
        spend_db_url=os.getenv('SPEND_DB_URL'),
        test_username=os.getenv('TEST_USERNAME'),
        test_password=os.getenv('TEST_PASSWORD')
    )


@pytest.fixture(scope='session')
def auth(envs):
    browser.open(envs.frontend_url)
    browser.element("a[href*='redirect']").click()
    browser.element("input[name='username']").set_value(envs.test_username)
    browser.element("input[name='password']").set_value(envs.test_password)
    browser.element("button[type='submit']").click()

    return browser.driver.execute_script('return window.sessionStorage.getItem("id_token")')


@pytest.fixture(scope='session')
def spends_client(envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture(scope='session')
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(params=[])
def spends(request, spends_client):
    test_spend = spends_client.add_spends(request.param)
    yield test_spend
    all_spends = spends_client.get_spends()
    if test_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([test_spend.id])


@pytest.fixture()
def main_page(auth, envs):
    browser.open(envs.frontend_url)


@pytest.fixture(params=[])
def category(request, spends_client, spend_db):
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.category
    spend_db.delete_category(category.id)