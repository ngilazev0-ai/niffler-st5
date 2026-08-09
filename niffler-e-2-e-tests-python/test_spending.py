from time import sleep

import requests
from selene import browser, be, have
from selenium.webdriver.support.expected_conditions import alert_is_present


def test_spending_title_exists():
    browser.open('http://frontend.niffler.dc/')
    browser.element("a[href*='redirect']").click()
    browser.element("input[name='username']").set_value("dima")
    browser.element("input[name='password']").set_value("dima_123_er")
    browser.element("button[type='submit']").click()



    browser.element('.main-content').should(have.text('History of spendings'))


def test_spending_should_be_deleted_after_table_action():
    url = 'http://gateway.niffler.dc:8090/api/spends/add'
    headers = {
        'Authorization': 'Bearer eyJraWQiOiIyNzdmODdmMy1mNjQ1LTRhNzMtYWI3NS0xNTUyZTRm'
                         'ZTlhOGMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJkaW1hIiwiYXVkIjoiY2'
                         'xpZW50IiwiYXpwIjoiY2xpZW50IiwiYXV0aF90aW1lIjoxNzg2Mjk3NjI1LC'
                         'Jpc3MiOiJodHRwOi8vYXV0aC5uaWZmbGVyLmRjOjkwMDAiLCJleHAiOjE3OD'
                         'YyOTk0MjUsImlhdCI6MTc4NjI5NzYyNSwianRpIjoiYzJhYTE1YWEtYmNjZC0'
                         '0MjRmLWE5YjAtMmMxMDkzMjQyNTEzIiwic2lkIjoiOEN4ZkhveC1yU2tmSG9M'
                         'cXk4U1Q4bHpuRlk2dk1QdlRlS21pbl9JSGpUVSJ9.rks7MCRSAasaEW0K-7IC'
                         'UODGsRDReTcRf5DYzanqBW1Cm_0oJfuCmKUePtDOvawsJksPCHEc2Q4CTgN48'
                         'kkoI_RXpu5-Pmvyd-DYBHzC0wIsMBJ41W1TI9eI4ZXy0LF_88oCCddhAudBDD'
                         'dlyKiG6BmuOtGUUBw8tHiKvh4gjdrANxA2AZrPLKT3D0DTKLlBIwo_1PWfP3eg'
                         'Dqi2rS7lGPk4uUnmdlACog-6SdbMtq7GRb8RGA2S1a1feNscGAHnVfNBOsJ6JN'
                         'gWW9J_pWFAWqRynhYy0V5_7eKrF-8cUSCM6Xg4BSxaX-y-IOrJq6ziMJt8Qghg'
                         'qDxadnjh5ZDmdA'
    }
    data = {
        "amount": "108.51",
        "description": "QA.GURU Advanced 5 - обучение",
        "category": "SCHOOL",
        "spendDate": "2026-08-09T17:53:15.741Z",
        "currency": "RUB"
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    print(response.json())


    browser.open('http://frontend.niffler.dc/')
    browser.element("a[href*='redirect']").click()
    browser.element("input[name='username']").set_value("dima")
    browser.element("input[name='password']").set_value("dima_123_er")
    browser.element("button[type='submit']").click()
    browser.element(".spendings-table tbody").should(have.text("QA.GURU Advanced 5 - обучение"))
    browser.element(".spendings-table tbody input[type='checkbox']").click()
    browser.element(".spendings__bulk-actions button").click()
    browser.all(".spendings-table tbody tr").should(have.size(0))

    browser.element(".spendings__content").should(have.text("No spendings provided yet!"))

