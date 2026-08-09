from time import sleep

from selene import browser as sel_browser
import pytest


@pytest.fixture
def browser() -> sel_browser:
    sel_browser.open('http://frontend.niffler.dc/')
    sel_browser.element("a[href*='redirect']").click()
    sel_browser.element("input[name='username']").set_value("dima")
    sel_browser.element("input[name='password']").set_value("dima_123_er")
    sel_browser.element("button[type='submit']").click()
    sleep(2)
    yield sel_browser
    sel_browser.quit()