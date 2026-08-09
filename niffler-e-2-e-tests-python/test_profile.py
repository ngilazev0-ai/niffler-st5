from time import sleep

from selene import have


class TestProfile:

    def test_profile_category_list(self, browser):
        browser.open('http://frontend.niffler.dc/profile')
        browser.element(".main-content__section-categories").should(have.text("All your spending categories"))

    def test_create_category(self, browser):
        browser.open('http://frontend.niffler.dc/profile')
        browser.element('input[name="category"]').set_value("Test_category")
        browser.element('.add-category__input-container button').click()
        browser.element('.categories__list').should(have.text("Test_category"))


