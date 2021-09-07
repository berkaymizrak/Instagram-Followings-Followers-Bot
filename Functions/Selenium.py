# Selenium Functions
# Berkay MIZRAK
# www.BerkayMizrak.com
# www.DaktiNetwork.com


try:
    import time
    import os
    import sys

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException

    from python3_anticaptcha import NoCaptchaTaskProxyless

    from Functions import File
    from Functions import String
    from Functions import Progress
except Exception as e:
    print()
    print(e)
    while True:
        input('\n! ! ERROR --> A module is not installed...')


# Scroll down all the way of page
def scroll_down(browser):
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll up all the way of page
def scroll_up(browser):
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll to the element by xpath on page
def move_to_element(browser, xpath):
    try:
        element = browser.find_element_by_xpath(xpath)
        browser.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(0.3)
    except:
        pass

# Go to the link and check the xpath given if element present on the page.
def check_page(browser, go, xpath='//*', second=5, error_times=3, error_loop=True, captcha_check=False):
    check_count = 0
    check_bool = True
    while check_bool:
        captcha_error_check = False
        check_count += 1 # Count each loop
        if check_count > error_times: # If number of loop more than 10, return definition
            print('\n--> Browser is re-opening because of too many browser errors.')
            browser.quit()
            break

        timeout = False
        try:
            browser.current_url  # to check if browser is still open, otherwise go to the Exception
            try:
                browser.get(go)
            except TimeoutException:
                timeout = True
                raise TimeoutException
            if captcha_check:
                r = captcha_finder(browser)
                if r:
                    # If there is captcha on the page, return def and then try to solve it in anyway you like
                    # (Solve it by automated way or manual)
                    return True
            WebDriverWait(browser, second).until(EC.presence_of_element_located((By.XPATH, xpath))) # wait for element to see on page
            check_bool = False  # page loaded, leave the def
        except TimeoutException:
            captcha_error_check = True
            # if error comes from loading page, will enter timeout,
            # otherwise error will come from the one which looks for element and error will goes to 'NOT TIMEOUT'
            if timeout:
                print("\n--> Page couldn't load in time (%s sec). Trying again..." % second)
                print()
                print('-' * 15)
            else:
                print("\n--> Desired element couldn't find on page. Trying again...")
                print()
                print('-' * 15)
        except Exception as e:
            captcha_error_check = True  # Page gave error so check if there is captcha on the page
            try:
                browser.current_url  # to check if browser is still open, otherwise show other message
                print("\n--> An error occurred while opening page. Trying again...")
            except:
                print("\n--> Browser closed. Opening again...")
            print('ERROR:')
            print(e)
            print()
            print('-' * 15)

            browser.current_url  # to check if browser is still open, otherwise will throw error to outside of def

        if captcha_check and captcha_error_check:
            r = captcha_finder(browser)
            if r:
                # If there is captcha on the page, return def and then try to solve it in anyway you like
                # (Solve it by automated way or manual)
                return True
        if not error_loop:
            # if user overwrite function not to reflesh page many times untill find the element desired by xpath, return
            return None
    return None

def turn_off_all_alerts(browser, accept=True, show_error=False, sound_for_error=False, exit_all=False):
    # options.add_argument("--disable-popup-blocking")  # This is argument for selenium browser to block everything
    try:
        alert = browser.switch_to.alert
        if accept:
            alert.accept()
        else:
            alert.dismiss()
    except Exception as e:
        if sound_for_error:
            Progress.sound_notify()
        if show_error:
            Progress.exit_app(e=e, exit_all=exit_all)

def captcha_finder(browser):
    src = browser.page_source
    captcha_found = False

    src = String.lower_string(src)  # Turkish lower function
    src = src.replace('robots', '')

    keywords = [
        'captcha-delivery.com',
        'alışılmadık bir trafik',
        'robot',
    ]
    if any(i in src for i in keywords):
        captcha_found = True

    if captcha_found:
        message = 'reCAPTCHA found in page (Might be robot test on page.).'
        print(message)
        return True
    else:
        return None

def captcha_solve(browser, cost_file='costs.txt', ANTICAPTCHA_KEY=None, save_cost=True, captcha_sound=True, domain=None):
    if not ANTICAPTCHA_KEY:
        ANTICAPTCHA_KEY = os.getenv('ANTICAPTCHA_KEY')

    if not domain:
        domain = browser.current_url

    xpath = '//*[@id = "g-recaptcha-response"]'
    try:
        browser.find_element_by_xpath(xpath)
        # Captcha found in page
        exist_captcha = True
    except:
        # Captcha CAN NOT found in page
        exist_captcha = False

    user_answer = None
    cost = 0
    start_time = time.time()
    if exist_captcha:
        if captcha_sound:
            Progress.sound_notify_times(times=1)
        print('--> reCAPTCHA solving. It might take some time, please wait...')
        key = ''
        try:
            SITE_KEY = None
            try:
                # TRY normal captcha box
                xpath = '//*[contains(@class,"g-recaptcha")]'
                captcha_box = browser.find_element_by_xpath(xpath)
                SITE_KEY = captcha_box.get_attribute('data-sitekey')
                if not SITE_KEY:
                    raise Exception
            except:
                # Normal captcha box COULD NOT BE FOUND. Find site key from new generation of reCAPTCHA
                xpath = '//iframe[contains(@role, "presentation")]'
                captcha_box = browser.find_element_by_xpath(xpath)
                captcha_src = captcha_box.get_attribute('src')
                if 'k=' in captcha_src and '&' in captcha_src:
                    captcha_src_list = captcha_src.split('&')
                    for i in captcha_src_list:
                        if i.startswith('k='):
                            SITE_KEY = i.replace('k=', '')
                            break
            if not SITE_KEY:
                raise Exception

            user_answer = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(
                anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
                websiteURL=domain, websiteKey=SITE_KEY)
            if 'errorDescription' in user_answer:
                raise Exception
            key = user_answer['solution']['gRecaptchaResponse']
            try:
                cost = user_answer['cost']
                cost = float(cost)
            except:
                cost = 0

            # Code worked untill here so there is no error.
            error_captcha = False
        except Exception as e:
            error_captcha = True
            message = '--> An error occurred while solving reCAPTCHA. Processing is in progress.'
            if 'errorDescription' in user_answer:
                message_from_system = user_answer['errorDescription']
                message = message + '\n' + str(message_from_system)
            Progress.exit_app(e=e, message=message, exit_all=False)

        if not error_captcha:
            if 'endTime' in user_answer and 'createTime' in user_answer:
                end_time = user_answer['endTime']
                create_time = user_answer['createTime']
                pass_time = end_time - create_time
            else:
                pass_time = time.time() - start_time

            print('\nCalculation time: %s' % Progress.time_definition(pass_time))
            print('reCAPTCHA solved. Price: $%s' % cost)

        if save_cost:
            if cost != 0 and isinstance(cost, (int, float)):
                read_record = File.read_records_to_list(txt_file=cost_file, file_not_found_error=False, exit_all=False)
                try:
                    balance = float(read_record[0])
                except:
                    balance = 0
                balance += cost
                File.save_records_list(txt_file=cost_file, records_list=[balance], overwrite=True, exit_all=False)

        # ADD SOLUTION TO THE PAGE.
        try:
            browser.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % key)
        except:
            pass

    return exist_captcha

# After solving reCAPTCHA, saving cookies and then reading them again might work for some pages.
"""
pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)
"""