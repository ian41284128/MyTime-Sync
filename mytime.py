from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from shift import Shift


def sign_in(driver, username, password, timeout=10):
    print("Signing in...")
    try:
        username_field = WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_element_located((By.ID, "submittedIdentifier"))
        )
        username_field.send_keys(username)
        driver.find_element(By.ID, "btnSignIn").click()
        print("username...")
        password_field = WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_element_located((By.ID, "password"))
        )
        password_field.send_keys(password)
        driver.find_element(By.ID, "btnSignIn").click()
        print("password!")
    except TimeoutException:
        return False
    else:
        return True


def get_shifts(driver, timeout=10):
    my_shifts = []
    print("Waiting for shifts to load...")
    shift_elements = WebDriverWait(driver, timeout).until(
        expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "shift"))
    )
    print("Shifts: ")
    for shift_element in shift_elements:
        date = shift_element.find_element(By.CLASS_NAME, "dayLabel").get_attribute("aria-label")
        time = shift_element.find_element(By.TAG_NAME, "time").get_attribute("aria-label")
        print(date, end=" from ")
        print(time)
        start = time.split('-')[0]
        end = time.split('-')[1].split('M')[0] + 'M'
        name = time.split('-')[1].split('M ')[1]
        my_shifts.append(Shift.create_from_mytime(date, start, end, name))
    return my_shifts


def init(url):
    options = Options()
    options.add_argument("--headless")
    print("Initializing selenium...")
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    return driver


def scrape(url, username, password, timeout=10):
    driver = init(url)
    if not sign_in(driver, username, password, timeout):
        driver.quit()
        exit(1)
    shifts = get_shifts(driver, timeout)
    print("Quitting selenium...")
    driver.quit()
    return shifts
