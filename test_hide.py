import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import InvalidSwitchToTargetException, WebDriverException
import pytest_check as check
import time
import logging

LOGGER = logging.getLogger(__name__)
seen = set()
current_window = None
@pytest.fixture(scope='module')
def driver():
    global current_window
    opts = webdriver.FirefoxOptions()
    prof = webdriver.FirefoxProfile()
    prof.set_preference('dom.max_script_run_time', 2)
    prof.set_preference('dom.max_chrome_script_run_time', 2)
    prof.set_preference('dom.enable_window_print', False)
    opts.add_argument('--headless')
    driver = webdriver.Firefox(options=opts, firefox_profile=prof)
    driver.get('http://localhost:666/fpsmpjournal/')
    current_window = driver.current_window_handle
    yield driver
    driver.quit()


class utils:
    """
    helper methods for test cases
    """
    @staticmethod
    def isSeen(link):
        global seen
        if link in seen:
            return True

        link = link.replace('http://localhost:666', '')
        for pages in seen:
            if link in pages:
                return True
        return False

    @staticmethod
    def returnToTab(driver, button):
        global current_window
        if driver.current_window_handle != current_window:
            current_window = driver.current_window_handle
            try:
                for handles in driver.window_handles:
                    if handles != current_window:
                        driver.switch_to(handles)
                        driver.close()

                driver.switch_to.window(current_window)
                print(f'{button} opened {driver.current_url}')
            except (InvalidSwitchToTargetException, WebDriverException):
                pass
    @staticmethod
    def is_header(driver):
        try:
            wait = WebDriverWait(driver, 60)
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'siteHeader')))
        except (WebDriverException):
            LOGGER.warning('caught exception in: ' + driver.current_url)
            return False
        return True

@pytest.mark.skip(reason='obsolete test')
def test_windowHandle(driver):
    global current_window
    assert current_window

def test_if_all_links_load(driver, button=None):
    global seen
    currentPage = driver.current_url
    
    LOGGER.info('visited to: ' + currentPage)
    if not 'localhost' in currentPage or not utils.is_header(driver):
        utils.returnToTab(driver, button)
        return

    if utils.isSeen(currentPage):
        return
    seen.add(currentPage)
    elements = driver.find_elements(By.TAG_NAME, 'a')

    
    LOGGER.info('executing loop in: ' + currentPage)
    for i in range(0, len(elements)):
        el = elements[i]
        link = driver.execute_script('return arguments[0].dataset.link', el)
       
        if el.get_attribute('onclick') or not link or utils.isSeen('http://localhost:666'+link):
            continue
        elemHTML = el.get_attribute('outerHTML')
        LOGGER.info(f'button: {elemHTML}\tcounter: {i}')
        driver.execute_script('arguments[0].click()', el)
        time.sleep(1.5)

        if 'localhost' in driver.current_url:
            check.is_true(utils.is_header(driver), 'header not found in: ' + driver.current_window_handle)
        

        test_if_all_links_load(driver, elemHTML)

        if driver.current_url != currentPage:
            driver.back()
            assert driver.current_url == currentPage

        elements = driver.find_elements(By.TAG_NAME, 'a')
        


@pytest.mark.skip()
@pytest.mark.parametrize('links', [
    #('http://localhost:666/fpsmpjournal/monthly/1811/introduction.html'),
    #('http://localhost:666/fpsmpjournal/monthly/2010/introduction.html'),
    #('http://localhost:666/fpsmpjournal/monthly/2010/education_02.html'),
    #('http://localhost:666/fpsmpjournal/monthly/2010/education.html'),
    #('http://localhost:666/fpsmpjournal/monthly/2008/education.html'),
    ('http://localhost:666/fpsmpjournal/monthly/2001/summary.html')
    ])
def test_specific(driver, links, button=None):
    utils.returnToTab(driver, button)
    driver.get(links)
    global seen, current_window
    currentPage = driver.current_url
    LOGGER.info(currentPage)
    if not 'localhost' in currentPage:
        assert driver.find_element_by_class_name('siteHeader')
        return

    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'siteHeader')))

    elements = driver.find_elements(By.TAG_NAME, 'a')
    check.is_true(utils.is_header(driver), 'header not found in: ' + driver.current_window_handle)
    
    for i in range(0, len(elements)):
        el = elements[i]
        link = driver.execute_script('return arguments[0].dataset.link', el)
       
        if el.get_attribute('onclick') or not link or utils.isSeen('http://localhost:666'+link):
            continue
        elemHTML = el.get_attribute('outerHTML')
        LOGGER.info(f'button: {elemHTML}\tcounter: {i}')
        current_window = driver.current_window_handle
        driver.execute_script('arguments[0].click()', el)
        time.sleep(1)

        if 'localhost' in driver.current_url:
            check.is_true(utils.is_header(driver), 'header not found in: ' + driver.current_window_handle)
        
        utils.returnToTab(driver, elemHTML)
        if driver.current_url != currentPage:
            driver.back()
            assert driver.current_url == currentPage

        elements = driver.find_elements(By.TAG_NAME, 'a')

# def test_null(driver):
#     driver.get('http://localhost:666/fpsmpjournal/monthly/2010/education_02.html')
#     el = driver.find_element_by_link_text('記事TOP')
#     driver.execute_script('arguments[0].click()', el)
#     utils.returnToTab(driver, el.get_attribute('outerHTML'))
#     wait = WebDriverWait(driver, 2)
#     wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'siteHeader')))

@pytest.mark.skip()
def test_expect():
    check.is_true(1 == 2, 'values do not match')
    LOGGER.warning('abcd')
    time.sleep(5)

def teardown():
    pass

if __name__ == '__main__':
    test_expect()