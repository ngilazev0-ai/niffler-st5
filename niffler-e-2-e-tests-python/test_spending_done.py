import requests
from selene import browser, have


def test_spending_title_exists():
    browser.open('http://frontend.niffler.dc')
    browser.element('a[href*=redirect]').click()
    browser.element('input[name=username]').set_value("stas")
    browser.element('input[name=password]').set_value("12345")
    browser.element('button[type=submit]').click()
    browser.element('.main-content').should(have.text('History of spendings'))


def test_spending_should_be_deleted_after_table_action():
    url = 'http://gateway.niffler.dc:8090/api/spends/add'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJraWQiOiJiNDE wNzM3ZC03OGU2LTQyZmItOGQ1YS0xNDhkYTJmYmU4NTIiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJzdGFzIiwiYXVkIjoiY2xpZW50IiwiYXpwIjoiY2xpZW50IiwiYXV0aF90aW1lIjoxNzIzMTQyMzY3LCJpc3MiOiJodHRwOi8vYXV0aC5uaWZmbGVyLmRjOjkwMDAiLCJleHAiOjE3MjMxNDQxNjcsImlhdCI6MTcyMzE0MjM2NywianRpIjoiODVjYTM5MTYtZWJkOC00MWJhLTg2NzAtZmZkYjgxYTY1YjY0Iiwic2lkIjoiVUFvcXlJd0I1Z1lJWjNtSnpKX05yNE5fNEtjam5jNk56WmZRRU9UQVQ3ZyJ9.FddaE5jL6d-fZ8GZt2VvnzxYPWngAsjF8d72b8dfOkI0ANvYZBDZM0zZE6X_mQVmXvCUFwFIjtp1TpetrU8NZ7EMcT61gJ-yTbJCrtzBrKaFqLzXp5Tr89nwhMZGRA2W4eVAI6zzz-I5Gq1jn11aAa6hzT-HkU9hbFT4JfA8J9iWNMLkALFvQFqO9CblhBYE-QmqTnWHFt2qGDX8VrRRoZ3-zACMns0PpWIHK8plkOSq3vxRqktjWmT9xVSCftDi4fJ1wkofmwl7NYaNaYxbQaPLVx9gY0ANRbYQWccodrVL2n8Vxc6UBZZcLrI8_wV7HMbSXAxm_4U40oDujPy1ng',
        'Content-Type': 'application/json',
        'Origin': 'http://frontend.niffler.dc',
    }
    data = {
        "amount": "108.51",
        "description": "QA.GURU Python Advanced 1",
        "category": "school",
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    print(response.json())

    browser.open('http://frontend.niffler.dc')
    browser.element('a[href*=redirect]').click()
    browser.element('input[name=username]').set_value("stas")
    browser.element('input[name=password]').set_value("12345")
    browser.element('button[type=submit]').click()

    browser.element('.spendings-table tbody').should(have.text("QA.GURU Python Advanced 1"))
    browser.element('.spendings-table tbody input[type=checkbox]').click()
    browser.element('.spendings__bulk-actions button').click()

    browser.all(".spendings-table tbody tr").should(have.size(0))
    browser.element('.spendings__content').should(have.text("No spendings provided yet!"))

