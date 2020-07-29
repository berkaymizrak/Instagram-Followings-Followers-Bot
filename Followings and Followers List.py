# -*- coding: utf-8 -*-
# Instagram Find Followings Who Doesn't Follow Back You
#  Berkay MIZRAK
# www.BerkayMizrak.com
# www.DaktiNetwork.com

# Get list of Followings who doesn't follow you and
# list of Followers who you don't follow

version = '1.1'
program = "Instagram Followings/Followers v%s" % version
code = 'instagram_follower_following'

print('\n\t%s' % (program))
print('\n\t\twww.BerkayMizrak.com')
print('\n\t\t\twww.DaktiNetwork.com')


try:
    import time
    import os

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import dotenv
    dotenv.load_dotenv()

    from Functions import Progress
    from Functions import File
    from Functions import Connect
    from Functions import Selenium
except Exception as e:
    print()
    print(e)
    while True:
        input('\n! ! ERROR --> A module is not installed...')


def scroll_div(num):
    xpath_scroll_elem = '//div[contains(@role, "dialog")]//div/ul/..'
    class_scroll = browser.find_element_by_xpath(xpath_scroll_elem).get_attribute('class')
    jscommand = """
    followers = document.querySelector(".%s");
    followers.scrollTo(0, followers.scrollHeight);
    var lenOfPage=followers.scrollHeight;
    return lenOfPage;
    """ % class_scroll
    lenOfPage = browser.execute_script(jscommand)
    match = False
    now = time.time()
    time.sleep(0.01)
    count = 0
    fetched = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = browser.execute_script(jscommand)
        num_current_follows = len(browser.find_elements_by_xpath("//a[contains(@class,'notranslate')]"))
        if lastCount == lenOfPage:
            if num > num_current_follows:
                fetched = False
            else:
                match = True
        else:
            fetched = True

        if fetched:
            count = 0
        else:
            count += 1
        Progress.progress(count=num_current_follows, total=num, now=now, message='Fetching...')
        if count > 15:
            print('\n--> It has been too long time that program could not fetch new data. Now will ignore and continue to process.')
            match = True


username = os.getenv("insta_username")
pwd = os.getenv("insta_pwd")

if not username:
    username = input('\nUsername: ')

if not pwd:
    while True:
        try:
            pwd = input('Password: ')

            if len(pwd) < 6:
                raise Exception

            break
        except:
            print('\n--> Password can not be shorter than 6 characters.')

while True:
    try:
        user = int(input("\n1: Your account\n"
                 "2: Anyone else's account\n"
                 "Whose account will be checked for followers? [select 1 or 2] "))

        if user not in [1, 2,]:
            raise Exception

        if user == 1:
            control_user = username
        else:
            control_user = input('\nPlease enter the username that will be checked: ')
        break
    except:
        print('\n--> Please select only showed numbers. [1 or 2]')


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'

# add path to create execution easily (using such as pyinstaller)
File._append_run_path()
driver = File.source_path('chromedriver.exe')

# Check if program has permission to run from developer by API
Connect.check_run(code, program, 30, sound_error=True)  # <-- Remove this line in your app or you can create yours.

while True:
    login_succesful = False
    try:
        print()
        print('-' * 40)
        print('\nStarting...')

        try:
            # Check if browser still open. If not, raise Exception and create Browser again.
            # In first loop, it will raise Exception and will create Browser first time.
            browser.current_url
        except Exception as e:
            options = webdriver.ChromeOptions()
            options.add_argument('user-agent={%s}' % user_agent)
            options.add_argument('--blink-settings=imagesEnabled=false')  # Remove images from pages to open fast
            browser = webdriver.Chrome(options=options, executable_path=driver)

        count_reflesh = 0
        while not login_succesful:
            count_reflesh += 1
            if count_reflesh > 3:
                browser.quit()
                message = 'Program shutting down because of errors.'
                Progress.exit_app(message=message, exit_all=True)

            # Go to the link and check the xpath given if element present on the page.
            url = 'https://www.instagram.com/accounts/login/'
            xpath = '//div[@id = "react-root"]'
            Selenium.check_page(browser, url, xpath, 10)

            try:
                WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.NAME, "username")))
            except:
                message = 'Login form could not be found on page. Will load again.'
                Progress.exit_app(message=message, exit_all=False)
                continue

            element_username = browser.find_element_by_name("username")
            element_password = browser.find_element_by_name("password")

            element_username.send_keys(username)
            element_password.send_keys(pwd)

            login_button = browser.find_element_by_xpath("//button[contains(@type,'submit')]")

            login_button.click()

            try:
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'coreSpriteKeyhole')]")))
            except:
                pass

            if url == browser.current_url:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "slfErrorAlert")))
                print('\nUsername or password wrong, please enter again: ')
                login_succesful = False

                username = input('Username: ')
                pwd = input('Password: ')
                if user == 1:
                    control_user = username

                continue

            url = 'https://www.instagram.com/'
            xpath = '//div[@id = "react-root"]'
            Selenium.check_page(browser, url, xpath, 10)

            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class,'notranslate')]")))
            print('\n--- Successfully Logged In! ---')
            login_succesful = True

        url = 'https://www.instagram.com/%s/' % control_user
        xpath = '//div[@id = "react-root"]'
        Selenium.check_page(browser, url, xpath, 10)

        try:
            xpath = "//a[contains(@href, '%s')]" % control_user.lower()
            WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, xpath))) # wait for element to see on page
        except:
            xpath = "//h2[contains(text(), 'Private')]"
            WebDriverWait(browser, 1.5).until(EC.presence_of_element_located((By.XPATH, xpath))) # wait for element to see on page
            browser.quit()
            message = 'No data found because user account is private. Program stopped.'
            Progress.exit_app(message=message, exit_all=True)

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'followers')]")))

        button_followers = browser.find_element_by_xpath("//a[contains(@href, 'followers')]")

        button_followers.click()

        xpath_scroll_elem = '//div[contains(@role, "dialog")]//div/ul/..'
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_scroll_elem)))

        num_followers = int(browser.find_element_by_xpath("//a[contains(@href, 'followers')]/span").text)
        num_following = int(browser.find_element_by_xpath("//a[contains(@href, 'following')]/span").text)

        print('\nAccount Followers are fetching. (%s Followers) It might take some time...' % num_followers)

        scroll_div(
            num=num_followers,
        )

        print('\n\nAccount Followers are calculating, please wait...')

        followers_list = list()
        followers = browser.find_elements_by_xpath("//a[contains(@class,'notranslate')]")

        now = time.time()
        for follower in followers:
            followers_list.append(follower.text)

            # Process counter in seconds.
            Progress.count_forward(now=now, message='Calculating...')

        followers_list.sort()

        print("\n --> " + str(len(followers_list)) + " followers successfully fetched. ")


        try:
            browser.find_element_by_xpath("//button[contains(text(),'Close')]").click()
        except:
            try:
                browser.find_element_by_xpath("//div[contains(@role, 'dialog')]//h1/following-sibling::div/button").click()
            except:
                browser.refresh()

        button_following = browser.find_element_by_xpath("//a[contains(@href, 'following')]")
        button_following.click()

        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_scroll_elem)))

        print('\nAccount Followings are fetching. (%s Followings) It might take some time...' % num_following)

        scroll_div(
            num=num_following,
        )

        print('\n\nAccount Followings are calculating, please wait...')

        followings_list = list()
        followings = browser.find_elements_by_xpath("//a[contains(@class,'notranslate')]")

        now = time.time()
        for following in followings:
            followings_list.append(following.text)

            # Process counter in seconds.
            Progress.count_forward(now=now, message='Calculating...')

        followings_list.sort()

        print("\n --> " + str(len(followers_list)) + " followings successfully fetched. ")

        browser.quit()

        followings_list_final = list()
        for person in followings_list:
            if person not in followers_list:
                followings_list_final.append(person)
            if person in followers_list:
                followers_list.remove(person)

        """
        print("\n-------- PEOPLE WHO YOU DON'T FOLLOW BACK --------")
        time.sleep(2)
        print()
        count = 0
        for follower in followers_list:
            count += 1
            print(str(count) + ') ' + follower)

        print("\n-------- PEOPLE WHO DOESN'T FOLLOW YOU BACK --------")
        time.sleep(2)
        print()
        count = 0
        for follower in followings_list_final:
            count += 1
            print(str(count) + ') ' + follower)
        """

        txt_file_followers = "insta-you-to-not-follow-back_%s.txt" % control_user
        File.save_records_list(txt_file=txt_file_followers, records_list=followers_list, overwrite=True, exit_all=False)

        txt_file_followings = "insta-not-folow-back-to-you_%s.txt" % control_user
        File.save_records_list(txt_file=txt_file_followings, records_list=followings_list_final, overwrite=True, exit_all=False)

        Progress.sound_notify_times(3)

        message = " %s people found who doesn't follow you back.\n" \
                  " %s people found who you don't follow back.\n" \
                  "NOTE: Besides, please check txt files in the folder of program.\n" \
                  " - %s\n" \
                  " - %s" % (len(followings_list_final), len(followers_list), txt_file_followers, txt_file_followings)

        Progress.exit_app(message=message, exit_all=True)
    except Exception as e:
        try:
            browser.quit()
        except:
            pass
        message = 'An error occurred. Will start again.'
        Progress.exit_app(e=e, message=message, exit_all=False)
        continue

