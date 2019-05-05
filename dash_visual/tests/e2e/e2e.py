import time

from seleniumbase import BaseCase
from selenium.webdriver.common.action_chains import ActionChains


class TempMapTests(BaseCase):

    def test_e2e(self):
        self.open("http://localhost:8080")
        self.assert_element("#temp-map")
        self.assert_element("#btn-avg")
        self.assert_element("#btn-high")
        self.assert_element("#btn-low")
        self.assert_element("#low-and-high")
        self.assert_element("#temp-kanto-map")
        self.assert_text("温度マップ", "h1")
        self.assert_text("全国の温度マップ", "h2")
        self.click("button#btn-avg")
        time.sleep(3)
        self.driver.save_screenshot("screenshots/screen1.png")
        self.click("button#btn-high")
        time.sleep(3)
        self.driver.save_screenshot("screenshots/screen2.png")
        self.click("button#btn-low")
        time.sleep(3)
        self.driver.save_screenshot("screenshots/screen3.png")
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_id("temp-map")).perform()
        actions.move_to_element(self.driver.find_element_by_id("temp-kanto-map")).perform()
        actions.move_to_element(self.driver.find_element_by_id("low-and-high")).perform()
        actions.move_to_element(self.driver.find_element_by_id("btn-low")).perform()
        actions.move_to_element(self.driver.find_element_by_id("temp-kanto-map")).perform()
        self.assert_element("#temp-timesearias")
        self.driver.save_screenshot("screenshots/screen4.png")
