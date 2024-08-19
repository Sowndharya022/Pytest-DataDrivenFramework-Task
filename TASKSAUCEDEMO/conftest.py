import pytest
from selenium import webdriver
import os
import time

SCREENSHOT_DIR='screenshot'


@pytest.fixture(scope="function")
def setup(request):
    driver=webdriver.Chrome()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    request.cls.driver=driver
    yield driver
    driver.quit()


def pytest_runtest_makereport(item,call):
    if call.when=='call' and call.excinfo is not None:
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)


            #capture screenshot
            driver=item.funcargs['setup']
            timestamp=time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot-{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")