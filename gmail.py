from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import getpass  # for password
import os
import time

# Default values for click position
xpos = 0  # xposition of the click
ypos = 0  # yposition of the click


# query = {"query_term": "", "no_of_times": 0}
# tabs = {"Primary": 0, "Social": 0, "Promotions": 0, "Forums": 0}
# is_otp_enabled = false
# skip_first_mail = 0

# Function that initializes the Chrome driver
def init_driver():
    # setting up chromedriver
    chromedriver = "/Users/admin/virtualenvs/gmail_cleaner/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.wait = WebDriverWait(driver, 30)  # 20 seconds of polling for page wait
    driver.implicitly_wait(30)  # 20 seconds of polling for every page wait #alternative code for above line

    return driver


# Function to take in user preferences for settings
def set_preferences(driver):
    # User account details
    username = input("Enter gmail id:")
    password = getpass.getpass("Enter password:")

    # set preferences
    ansotp = input("Is 2 step verification enabled using OTP for this site (Y/N)")
    is_otp_enabled = (True if ansotp == 'Y' else False)  # if using OTP in account

    # tabs specifies the number of times delete action must be performed on each tab
    tabs = {"Primary": 0, "Social": 1, "Promotions": 0, "Forums": 0}

    try:
        skip_first_mail = input("How many initial mail pages to skip?")
        skip_first_mail = int(skip_first_mail)  # Convert to int
        ans = input("Would you like to delete Tabs(T) or Query(Q)")
        if ans == 'Q':
            try:
                query = {"query_term": "", "no_of_times": 0}  # Initializing query
                query["query_term"] = input("Enter Search Query: ")
                try:
                    query["no_of_times"] = int(
                        input("Enter Number of times to repeat action: "))  # Convert input into integer
                except ValueError:
                    raise ValueError
                except Exception as e:
                    raise e
                driver = run_login(driver, username, password, is_otp_enabled)  # invoke run_login()
                return run_lookup(driver, query, skip_first_mail)  # invoke run_lookup()
            except ValueError:
                raise ValueError

        elif ans == 'T':
            # Give selection for Tabs
            for i in tabs.keys():
                ans = input("Would you like to delete mails in " + i + "tab (Y/N)? :")
                if ans == 'Y':
                    try:
                        tabs[i] = input("Enter Number of times to repeat action for " + i + " tab :")
                    except ValueError:
                        raise ValueError
                    except Exception as e:
                        raise e
                else:
                    tabs[i] = 0  # don't execute action
            print("Executing Tabs:", tabs)
            driver = run_login(driver, username, password, is_otp_enabled)  # invoke run_login()
            return run_tabs(driver, tabs, skip_first_mail)  # invoke run_tabs() function
        else:
            print("ERROR: Incorrect response")
            time.sleep(3)  # Wait for user
            driver.close()  # Close the driver
            exit()
    except Exception as e:
        skip_first_mail = 0
        raise e


# ACTION DEFINITIONS
# Perform skip first few pages of mails
def action_skip_few_mails(driver, skip_first_mail):
    try:
        for x in range(skip_first_mail):
            # Clicking on Older Button
            # elem = driver.find_element_by_xpath("//div[@aria-label='Older']")  # alternative code for the below line
            elem = driver.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='Older']")))
            ac = ActionChains(driver)
            ac.move_to_element(elem).move_by_offset(xpos, ypos).click().perform()
            print("Click on Older mail button has been performed!")
            time.sleep(3)  # Wait for page to reload
    except TimeoutError:
        print("Could not perform skip mails action")
        raise TimeoutError
    except Exception as e:
        raise e
    return driver


# Perform select all action
def action_selectall_mails(driver):
    try:
        # Clicking on select all mails
        # elem = driver.find_element_by_xpath("//span[@role='checkbox']") #alternative code for the below line
        # elem = driver.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@role='checkbox']"))) #alternative code
        size = len(driver.find_elements_by_xpath("//span[@role='checkbox']"))
        print("size:", size)
        elem = driver.find_elements_by_xpath("//span[@role='checkbox']")
        elem[size - 1].click()  # perform click
        # ac = ActionChains(driver) #alternative code for above line
        # ac.move_to_element(elem).move_by_offset(xpos, ypos).click().perform() #alternative code for above line
        print("Click on select all mails has been performed!")
    except TimeoutError:
        print("Couldn't perform select_all action")
        raise TimeoutError
    except Exception as e:
        raise e
    return driver


# Perform delete button click action
def action_delete_mails(driver):
    try:
        # Clicking on Delete Button
        # elem = driver.find_element_by_xpath("//div[@aria-label='Delete']") #alternative code for the below line
        elem = driver.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Delete']")))
        ac = ActionChains(driver)
        ac.move_to_element(elem).move_by_offset(xpos, ypos).click().perform()
        print("Click on Delete button has been performed!")
    except TimeoutError:
        print("Couldn't perform delete action")
        raise TimeoutError
    except Exception as e:
        raise e
    return driver


# RUN DEFINITIONS

# Function to login into account
def run_login(driver, username, password, is_otp_enabled):
    try:
        # Loading website
        driver.get("http://mail.google.com")
        # assert "Gmail Login" in driver.title
        # elem = driver.find_element_by_name("identifier") #alternative code for the below line
        elem = driver.wait.until(EC.presence_of_element_located((By.NAME, "identifier")))
        elem.send_keys(username)
        print("Username entered")
        # elem = driver.find_element_by_id("identifierNext") #alternative code for the below line
        elem = driver.wait.until(EC.presence_of_element_located((By.ID, "identifierNext")))
        elem.click()
        print("Next button pressed")
        # elem = driver.find_element_by_name("password") #alternative code for the below line
        elem = driver.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        elem.send_keys(password)
        print("Password Entered")
        elem.send_keys(Keys.RETURN)
        print("Login button pressed")
        if (is_otp_enabled == True):
            otp = input("Please enter OTP: ")
            wait = WebDriverWait(driver, 2)
            # elem = driver.find_element_by_name("idvPin") #alternative code for the below line
            elem = driver.wait.until(EC.presence_of_element_located((By.NAME, "idvPin")))
            elem.send_keys(otp)
            elem.send_keys(Keys.RETURN)
            print("OK button pressed")
    except TimeoutError:
        raise TimeoutError
    except Exception as e:
        raise e
    return driver


# Function to lookup a search term and delete mails from results returned
def run_lookup(driver, query, skip_first_mail):
    try:
        # Search Query
        # elem = driver.find_element_by_xpath("//input[@aria-label='Search']") # alternative code for the below line
        elem = driver.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search']")))
        elem.send_keys(query["query_term"])
        elem.send_keys(Keys.RETURN)
        print("Search Query has been executed!")
        time.sleep(10)  # Wait for some time
        driver = action_skip_few_mails(driver, skip_first_mail)  # skip first mail action
        time.sleep(3)
        driver.switch_to_default_content()
        for x in range(query["no_of_times"]):
            driver = action_selectall_mails(driver)  # select all click action
            time.sleep(5)
            driver = action_delete_mails(driver)  # delete button click action
    except TimeoutError:
        raise TimeoutError
    except Exception as e:
        raise e
    return driver


# Function to delete mails from under particular tabs
def run_tabs(driver, tabs, skip_first_mail):
    # Run for all respective tabs
    try:
        for i in tabs.keys():
            if int(tabs[i]) > 0:
                try:
                    if i == "Social":
                        # Clicking on Social Tab
                        # elem = driver.find_element_by_xpath("//div[@aria-label='Social']") #alternative code for the below line
                        elem = driver.wait.until(
                            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Social']")))
                        ac = ActionChains(driver)
                        ac.move_to_element(elem).move_by_offset(xpos, ypos).click().perform()
                        print("Click on Social Tab has been performed!")

                    elif i == "Promotions":
                        # Clicking on Promotions Tab
                        # elem = driver.find_element_by_xpath("//div[@aria-label='Promotions']") #alternative code for the below line
                        elem = driver.wait.until(
                            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Promotions']")))
                        ac = ActionChains(driver)
                        ac.move_to_element(elem).move_by_offset(xpos, ypos).click().perform()
                        print("Click on Promotions Tab has been performed!")

                    elif i == "Updates":
                        # Clicking on Updates Tab
                        # elem = driver.find_element_by_xpath("//div[@aria-label='Updates']") #alternative code for the below line
                        elem = driver.wait.until(
                            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Updates']")))
                        ac = ActionChains(driver)
                        ac.move_to_element(elem).move_by_offset(xpos, ypos).click().perform()
                        print("Click on Updates Tab has been performed!")

                    elif i == "Forums":
                        # Clicking on Forums Tab
                        # elem = driver.find_element_by_xpath("//div[@aria-label='Forums']") #alternative code for the below line
                        elem = driver.wait.until(
                            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Forums']")))
                        ac = ActionChains(driver)
                        ac.move_to_element(elem).move_by_offset(xpos, ypos).click().perform()
                        print("Click on Forums Tab has been performed!")

                    elif i == "Primary":
                        # Clicking on Promotions Tab
                        # elem = driver.find_element_by_xpath("//div[@aria-label='Primary']") #alternative code for the below line
                        elem = driver.wait.until(
                            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Primary']")))
                        ac = ActionChains(driver)
                        ac.move_to_element(elem).move_by_offset(xpos, ypos).click().perform()
                        print("Click on Primary Tab has been performed!")

                    driver = action_skip_few_mails(driver, skip_first_mail)  # skip first mail action
                    time.sleep(2)

                    for j in range(int(tabs[i])):
                        driver = action_selectall_mails(driver)  # select all mail action

                        time.sleep(2)
                        driver = action_delete_mails(driver)  # delete mail action

                        time.sleep(5)  # Wait for page to load

                except TimeoutError:
                    raise TimeoutError
                except Exception as e:
                    raise e
    except Exception as e:
        raise e
    return driver


if __name__ == "__main__":
    driver = init_driver()
    set_preferences(driver)
    time.sleep(5)
    driver.quit()
