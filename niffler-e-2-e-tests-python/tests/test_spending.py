from selene import browser, have, command
from marks import Pages, TestData


@Pages.main_page
def test_spending_title_exists():
    browser.element('.main-content').should(have.text('History of spendings'))



TEST_CATEGORY = 'SCHOOL'

@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "108.51",
    "description": "QA.GURU Advanced 5 - обучение",
    "category": TEST_CATEGORY,
    "spendDate": "2026-08-09T17:53:15.741Z",
    "currency": "RUB"
})
def test_spending_should_be_deleted_after_table_action(category, spends):
    browser.element(".spendings-table tbody").should(have.text("QA.GURU Advanced 5 - обучение"))
    browser.element(".spendings-table tbody input[type='checkbox']").perform(command.js.scroll_into_view).click()
    browser.element(".spendings__bulk-actions button").click()
    browser.all(".spendings-table tbody tr").should(have.size(0))

    browser.element(".spendings__content").should(have.text("No spendings provided yet!"))

