# Connection Functions
# Berkay MIZRAK
# www.BerkayMizrak.com
# www.DaktiNetwork.com


try:
    import time
    import random
    import os
    import sys

    import requests
    import json
    import ast
    # from lxml import html, etree
    import logging

    import smtplib
    import ipaddress

    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from io import StringIO
    from email.mime.base import MIMEBase
    from email import encoders

    from os.path import basename

    from Functions import File
    from Functions import Progress
    from Functions import String

    import dotenv
    env_file = File.source_path('.env')  # for creating execution with pyinstaller.
    dotenv.load_dotenv(env_file)
except Exception as e:
    print()
    print(e)
    while True:
        input('\n! ! ERROR --> A module is not installed...')

def connect_api(https=True, domain=None, endpoint='api/external_program/', code='all', program='', inform_user_periodically=False, show_error=False, sound_error=False, exit_all=False, extra_data={}):
    if not domain:
        domain = os.getenv("domain")

    start = time.time()
    time.sleep(0.01)
    x = 0
    db_settings_dict = {}
    if https:
        url_first = 'https'
    else:
        url_first = 'http'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'

    while True:
        try:
            x += 1
            url = '%s://%s/%s' % (url_first, domain, endpoint)

            # Define, if needed (User-Agent, Accept, Referer etc.)
            headers = {
                "User-Agent": user_agent,
                # 'accept': '*/*',
                # 'accept-encoding': 'gzip, deflate, br',
                # 'accept-language': 'en-US,en;q=0.9,tr;q=0.8,pl;q=0.7',
            }
            if endpoint == 'api/external_program/':
                data = {
                    'key': code,
                    'program': program,
                }
                data.update(extra_data)
            else:
                data = {}

            response = requests.request("GET", url, headers=headers, data=data, timeout=10)
            response.encoding = 'UTF-8'
            response = response.json()

            # My API returns a dictionary which have 'ayar' and 'parametre' in keys.
            if code == 'all':
                if endpoint == 'api/external_program/':
                    for setting in response:
                        parameter = setting['parametre']
                        parameter = String.from_string_to_type(parameter.lower, 'try_all')

                        db_settings_dict[setting['ayar']] = parameter
                else:
                    db_settings_dict = response

                return db_settings_dict
            else:
                if len(response) and response:
                    response = String.from_string_to_type(response, 'try_all')

                return response

        except Exception as e:
            if inform_user_periodically:
                if x % 2 == 0:
                    message = '\nAn error occurred while running, trying again...'
                    print()
                    print('-' * 40)
                    print(message)
                    print()
            if x >= 3:
                end = time.time()
                passed_time = end - start
                message = 'An error occurred while running program. Please try again.\n' \
                        '(Trying time: %s)' % Progress.time_definition(passed_time)
                if sound_error:
                    Progress.sound_notify()
                if show_error:
                    Progress.exit_app(message=message, exit_all=exit_all)
                    print()
                else:
                    if exit_all:
                        Progress.exit_app(exit_all=exit_all)
                break

def check_run(program_code, program='', reload_time=30, sound_error=True):
    # This def checks API and get the value of 'program_code'.
    # if program_code is True, def returns
    # else, def stucks untill program_code comes as True.

    message_pasted = False
    length_of_last_message = 0
    length_of_last_message_MAX = 0
    while True:
        try:
            run = connect_api(code=program_code, program=program)  # Mostly returns True or False Boolean up to what you set on API
            if run != True:  # run only if "run" is True.
                run = None
        except Exception as e:
            run = None

        if run:
            if message_pasted:
                # If there was "False calistir" and 'count down' printed,
                # paste space as much as pasted text before.
                # Because after pyinstaller execution, print flush prints in bad view.
                message = 'Program is working now.'
                length_of_new_message = len(message)
                if length_of_last_message - length_of_new_message > 0:
                    message = message + ' ' * (length_of_last_message_MAX - length_of_new_message)
                print("\r%s" % message, flush=True, end="")
                print()
                print('-' * 40)
                print()
            # Continue to run main program (RETURN DEF)
            break
        else:
            if not message_pasted:
                print()
                print('-' * 10)
                print()
                if sound_error:
                    Progress.sound_notify()
            message_pasted = True

            now = time.time()
            time.sleep(0.01)
            message = ''
            while time.time() - now < reload_time:
                remaining_time = int(reload_time - (time.time() - now))
                net_time_string = Progress.time_definition(remaining_time)
                message = '--> An error occurred while running program. Trying again in %s.' % net_time_string
                print("\r%s" % message, flush=True, end="")
                time.sleep(1)
            length_of_last_message = len(message)
            if length_of_last_message_MAX < length_of_last_message:
                length_of_last_message_MAX = length_of_last_message


def send_email(message, subject, recipients, attach_file_name=None, attach_file_text=None, login_mail=None, pwd=None,
               sender='Email Sender', sound_error=True, show_error=True, exit_all=False, debug_mode=0):

    if not login_mail:
        login_mail = os.getenv('login_mail')
    if not pwd:
        pwd = os.getenv('pwd')

    try:
        msg = MIMEMultipart()

        msg['Subject'] = subject
        msg['From'] = sender
        recipient = ", ".join(recipients)
        msg['To'] = recipient

        msg.attach(MIMEText(message))

        if attach_file_name and attach_file_text:
            f = StringIO()
            # write some content to 'f'
            f.write(attach_file_text)
            f.seek(0)

            attach = MIMEBase('application', "octet-stream")
            attach.set_payload(f.read())
            encoders.encode_base64(attach)

            attach.add_header('Content-Disposition',
                           'attachment',
                           filename=attach_file_name)
            msg.attach(attach)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(debug_mode)  # Prints all process if debug == 1
        server.ehlo()
        server.starttls()

        server.ehlo()
        server.login(login_mail, pwd)

        # Send the email
        server.sendmail(sender, recipients, msg.as_string())
        server.close()
        return True
    except Exception as e:
        if sound_error:
            Progress.sound_notify()

        if show_error:
            message = '--> An error occurred while sending email.'
            Progress.exit_app(e=e, message=message, exit_all=exit_all)
        else:
            Progress.exit_app(e=e, exit_all=exit_all)

        return False


def get_proxy(selenium=True, get_random=True, count_loop=1, save_false_proxies=True, error_file='Recorded FALSE Proxies.txt',
              save_ok_proxies=True, ok_file='Recorded OK Proxies.txt', number_of_min_saved_proxies=20, number_of_save_proxies=40,
              run_test=True, test_header=None, test_url=None, test_timeout=1, sound_error=True, allow_print=True, no_proxy=True, for_https=True):
    # You can use this function with whether count_loop or get_random.
    # count_loop helps you to run it in while with using count_loop+=1 and you can receive proxies 1 by 1 in lines of proxy file.
    # if get_random set True, you get proxy randomly from proxy file without looking count_loop.
    if get_random:
        count_loop = random.randint(1, 101)

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
    header = {"User-Agent": user_agent}

    if run_test:
        if not test_header:
            test_header = header

        if not test_url:
            url = 'https://api.myip.com/'
            # url = 'https://api.ipify.org/'
        else:
            url = test_url

        if for_https:
            if url.lower().startswith('http://'):
                url = url.lower().replace('http://', 'https://', 1)
        else:
            if url.lower().startswith('https://'):
                url = url.lower().replace('https://', 'http://', 1)

    proxy_decide = ''
    url_proxies = [
        'https://hidemy.name/tr/proxy-list/?type=s#list',
        'https://www.us-proxy.org/',
        'https://www.sslproxies.org/',
    ]
    again = True
    force_scrap = False
    while again:
        random_proxy = random.randint(0, len(url_proxies)-1)
        url_proxy = url_proxies[random_proxy]
        check_internet = True  # will use this to check internet connection without proxy only once.
        count_loop += 1
        again = False  # will leave while unless again defined True

        if count_loop % 10 == 0 and no_proxy:
            # def will return NON-PROXY each 10 times

            if allow_print:
                print('Default proxy settings setted.')
            if selenium:
                proxy_decide = '--no-proxy-server'
            else:
                proxy_decide = {}

            record_ip_type = ''
        else:
            # def will return NON-PROXY each 10 times

            error_ip_list = File.read_records_to_list(error_file, file_not_found_error=False, exit_all=False)
            ok_ip_list = File.read_records_to_list(ok_file, file_not_found_error=False, exit_all=False)
            ok_ip_save_list = []
            for i in ok_ip_list:
                ok_ip_save_list.append(i)
            if ((len(ok_ip_list) < number_of_min_saved_proxies) and save_ok_proxies) or force_scrap:
                # if number saved proxies to the file less than minimum required number of proxies,
                # will crawl more new proxies.
                check_internet = False  # internet connection checked, so will not check it in next commands.
                internet_connection(timeout=4, reload_time=30, wait_for_network=True, sound_error=sound_error)
                try:
                    print('Proxies are grabbed:')
                    print(url_proxy)
                    page = requests.get(url_proxy,
                                        headers=header,
                                        timeout=4,
                                        )
                except:
                    message = 'Error occurred while crawling new proxies.'
                    logging.log(logging.ERROR, message)
                    if allow_print:
                        print('\n--> ' + message)
                    again = True
                    count_loop -= 1

                    # continue to loop until get the new proxies.
                    continue

                tree = html.fromstring(page.content)
                if 'hidemy.name' in url_proxy:
                    ips = tree.xpath('//div[@class = "table_block"]/table//tbody/tr/td[1]')  # list of all ips
                    ports = tree.xpath('//div[@class = "table_block"]/table//tbody/tr/td[2]')  # list of all ports
                    types = tree.xpath('//div[@class = "table_block"]/table//tbody/tr/td[5]')  # list of all types
                elif 'us-proxy' in url_proxy:
                    ips = tree.xpath('//div[contains(@class, "fpl-list")]//table//tr/td[1]')  # list of all ips
                    ports = tree.xpath('//div[contains(@class, "fpl-list")]//table//tr/td[2]')  # list of all ports
                    types = tree.xpath('//div[contains(@class, "fpl-list")]//table//tr/td[7]')  # list of all types
                elif 'sslproxies' in url_proxy:
                    ips = tree.xpath('//div[contains(@class, "fpl-list")]//table//tr/td[1]')  # list of all ips
                    ports = tree.xpath('//div[contains(@class, "fpl-list")]//table//tr/td[2]')  # list of all ports
                    types = tree.xpath('//div[contains(@class, "fpl-list")]//table//tr/td[7]')  # list of all types
                count_ip = 0
                if len(ips) == len(ports) == len(types):
                    pass
                else:
                    again = True
                    count_loop -= 1

                    # continue to loop untill get the new proxies.
                    continue

                for ip, port, type in zip(ips, ports, types):
                    # if ip.text and port.text and type.text:
                    #     pass
                    # else:
                    #     continue
                    add_type = ''
                    if 'hidemy.name' in url_proxy:
                        if 'http' in type.text.lower():
                            if add_type:
                                add_type += ','
                            add_type += 'HTTP'
                        if 'https' in type.text.lower():
                            if add_type:
                                add_type += ','
                            add_type += 'HTTPS'
                    elif 'us-proxy' in url_proxy:
                        add_type += 'HTTP'
                        if 'yes' in type.text.lower():
                            add_type += ',HTTPS'
                    elif 'sslproxies' in url_proxy:
                        add_type += 'HTTP'
                        if 'yes' in type.text.lower():
                            add_type += ',HTTPS'
                    if add_type:
                        add_type = ',' + add_type
                    else:
                        continue  # NO HTTP OR HTTPS PROXY (Such as Socks4, Socks5 proxy)
                    ip_from_page = ip.text.replace(' ', '')
                    add_ip_type = '%s:%s%s' % (ip_from_page, port.text, add_type)
                    try:
                        ipaddress.ip_address(ip_from_page)
                    except:
                        continue

                    if save_false_proxies:
                        # check if new proxy is not one of the proxies which doesn't work.

                        if add_ip_type not in error_ip_list:
                            if save_ok_proxies:
                                if add_ip_type not in ok_ip_save_list:
                                    count_ip += 1
                                    ok_ip_save_list.append(add_ip_type)
                            else:
                                count_ip += 1
                                ok_ip_save_list.append(add_ip_type)
                    else:
                        if save_ok_proxies:
                            # add our new proxy to the list of all proxies to save this in our proxy file in the future.
                            if add_ip_type not in ok_ip_save_list:
                                count_ip += 1
                                ok_ip_save_list.append(add_ip_type)

                if save_ok_proxies:
                    if len(ok_ip_save_list) > number_of_save_proxies:
                        ok_ip_save_list_new = random.sample(ok_ip_save_list, number_of_save_proxies)
                        for elem in ok_ip_save_list:
                            elem_types = elem.split(',')[1:]
                            if 'HTTPS' in elem_types:
                                if elem not in ok_ip_save_list_new:
                                    ok_ip_save_list_new.append(elem)
                        ok_ip_save_list = ok_ip_save_list_new
                    File.save_records_list(ok_file, ok_ip_save_list, overwrite=True, exit_all=False)

            http_count = 0
            https_count = 0
            for elem in ok_ip_save_list:
                elem_types = elem.split(',')[1:]
                if 'HTTP' in elem_types:
                    http_count += 1
                if 'HTTPS' in elem_types:
                    https_count += 1
            if https_count <= 3 or http_count <= 3:
                again = True
                force_scrap = True
                count_loop -= 1
                continue
            else:
                force_scrap = False

            if not len(ok_ip_save_list):
                again = True
                message = "Proxy couldn't get. Trying again..."
                Progress.exit_app(message=message, exit_all=False)
                continue

            if get_random:
                record_ip_type = random.choice(ok_ip_save_list)
            else:
                # Remaining calculated to get a proxy from our list, from LAST to FIRST.
                remaining = count_loop % len(ok_ip_save_list)
                remaining = len(ok_ip_save_list) - remaining
                if remaining >= len(ok_ip_save_list):
                    remaining = 0

                record_ip_type = ok_ip_save_list[remaining]
            record_ip_type = record_ip_type.replace(' ', '')
            record_ip_type = record_ip_type.replace('\n', '')
            record_ip = record_ip_type.split(',', 1)[0]
            record_types = record_ip_type.split(',')[1:]
            record_ip_list = record_ip.split(':')
            if len(record_ip_list) != 2:
                message = "Proxy doesn't work. Next proxy is testing...\n" \
                          "IP-Port: %s" % record_ip
                if not get_random:
                    message += "\tProxy Number: %s" % (remaining)
                if allow_print:
                    print(message)
                    print()
                again = True
                if save_false_proxies:
                    File.write_ok_and_false_proxy(record_ip_type, error_file=error_file, ok_file=ok_file)
                continue

            if for_https:
                if 'HTTPS' not in record_types:
                    again = True
                    continue
            else:
                if 'HTTP' not in record_types:
                    again = True
                    continue

            ip = record_ip_list[0]
            port = record_ip_list[1]

            proxy_decide = {}
            for type in record_types:
                proxy_decide[type.lower()] = "http://%s" % record_ip

            if save_false_proxies:
                if record_ip_type in error_ip_list:
                    File.write_ok_and_false_proxy(record_ip_type, error_file=error_file, ok_file=ok_file)
                    again = True
                    continue

            if run_test:
                try:
                    if check_internet:
                        internet_connection(timeout=test_timeout, reload_time=30, wait_for_network=True, sound_error=sound_error)

                    response = requests.get(url, proxies=proxy_decide, timeout=test_timeout, stream=True, headers=test_header)
                    if test_url:
                        # if any url overwritten on def, just check the status code.
                        if response.status_code != 200:
                            raise Exception
                    else:
                        response = response.json()
                        if response == {}:
                            raise Exception
                    if save_ok_proxies:
                        File.save_records_list(ok_file, ok_ip_save_list, overwrite=True, exit_all=False)
                except Exception as e:
                    message = "Proxy doesn't work. Next proxy is testing...\n" \
                              "IP: %s\tPort: %s" % (ip, port)
                    if not get_random:
                        message += '\tProxy Number: %s' % remaining
                    if allow_print:
                        print(message)
                        print()
                    again = True
                    if save_false_proxies:
                        File.write_ok_and_false_proxy(record_ip_type, error_file=error_file, ok_file=ok_file)
                    continue

            if selenium:
                proxy_decide = '--proxy-server=%s:%s' % (ip, port)
            else:
                # proxy_decide defined above.
                pass

            if allow_print:
                if get_random:
                    print("Proxy activated.\nIP: %s\tPort: %s" % (ip, port))
                else:
                    print("Proxy activated. Proxy Number: %s.\nIP: %s\tPort: %s" % (count_loop, ip, port))

    if allow_print:
        print()
    if get_random:
        return proxy_decide, record_ip_type
    else:
        return count_loop, proxy_decide, record_ip_type
# USAGE GET PROXY -----------------------
"""
proxy_decide, curl = get_proxy(selenium=False, get_random=True, run_test=False)  # OPTION 1
count_loop += 1  # OPTION 2
count_loop, proxy_decide, curl = get_proxy(selenium=False, get_random=False, count_loop=count_loop, run_test=False)  # OPTION 2
response = requests.get(
    url,
    headers={},
    stream=True,
    proxies=proxy_decide,
    timeout=5,
)
"""
# USAGE GET PROXY -----------------------


def get_proxy_orbit(selenium=True, get_random=True, count_loop=1, save_false_proxies=True, error_file='Recorded FALSE Orbit Proxies.txt',
              save_ok_proxies=True, ok_file='Recorded OK Orbit Proxies.txt', number_of_min_saved_proxies=7, number_of_save_proxies=15,
              run_test=True, test_header=None, test_url=None, test_timeout=1, sound_error=True, allow_print=True, no_proxy=True, for_https=True, API_KEY=''):
    # You can use this function with whether count_loop or get_random.
    # count_loop helps you to run it in while with using count_loop+=1 and you can receive proxies 1 by 1 in lines of proxy file.
    # if get_random set True, you get proxy randomly from proxy file without looking count_loop.
    if allow_print:
        print()
        print('--> Proxy scraper is started.')
        print()
    if get_random:
        count_loop = random.randint(1, 101)
    if number_of_save_proxies < 2:
        number_of_save_proxies = 2  # Proxy Orbit send as list when count is more than 1

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
    header = {"User-Agent": user_agent}

    url = ''
    if run_test:
        if not test_header:
            test_header = header

        if not test_url:
            url = 'https://api.myip.com/'
            # url = 'https://api.ipify.org/'
        else:
            url = test_url

        if for_https:
            if url.lower().startswith('http://'):
                url = url.lower().replace('http://', 'https://', 1)
        else:
            if url.lower().startswith('https://'):
                url = url.lower().replace('https://', 'http://', 1)

    proxy_decide = ''
    again = True
    curl = ''
    while again:
        url_proxy = "http://api.proxyorbit.com/v1/"
        url_proxy += '?ssl=%s' % str(for_https).lower()
        url_proxy += '&protocols=http'
        url_proxy += '&count=%s' % number_of_save_proxies
        url_proxy += '&token=%s' % API_KEY
        check_internet = True  # will use this to check internet connection without proxy only once.
        count_loop += 1
        again = False  # will leave while unless again defined True

        if count_loop % 10 == 0 and no_proxy:
            # def will return NON-PROXY each 10 times

            if allow_print:
                print('Default proxy settings setted.')
            if selenium:
                proxy_decide = '--no-proxy-server'
            else:
                proxy_decide = {}
        else:
            # def will return NON-PROXY each 10 times

            error_ip_list = File.read_records_to_list(error_file, file_not_found_error=False, exit_all=False)
            ok_ip_list = File.read_records_to_list(ok_file, file_not_found_error=False, exit_all=False)
            ok_ip_save_list = []
            for i in ok_ip_list:
                ok_ip_save_list.append(i)
            if ((len(ok_ip_list) < number_of_min_saved_proxies) and save_ok_proxies):
                # if number saved proxies to the file less than minimum required number of proxies,
                # will crawl more new proxies.
                check_internet = False  # internet connection checked, so will not check it in next commands.
                internet_connection(timeout=4, reload_time=30, wait_for_network=True, sound_error=sound_error)
                try:
                    message = 'Proxies are grabbed.'
                    logging.log(logging.INFO, message + '  |  URL: %s' % url_proxy)
                    if allow_print:
                        print(message)
                        print()
                    resp = requests.get(url_proxy)
                    resp = resp.json()
                except:
                    message = 'Error occurred while crawling new proxies.'
                    logging.log(logging.ERROR, message)
                    if allow_print:
                        print('\n--> ' + message)
                    again = True
                    count_loop -= 1
                    Progress.count_down(30)

                    # continue to loop until get the new proxies.
                    continue

                curls = []
                for pr in resp:
                    curls.append(pr['curl'])
                count_ip = 0

                for curl in curls:
                    if save_false_proxies:
                        # check if new proxy is not one of the proxies which doesn't work.

                        if curl not in error_ip_list:
                            if save_ok_proxies:
                                if curl not in ok_ip_save_list:
                                    count_ip += 1
                                    ok_ip_save_list.append(curl)
                            else:
                                count_ip += 1
                                ok_ip_save_list.append(curl)
                    else:
                        if save_ok_proxies:
                            # add our new proxy to the list of all proxies to save this in our proxy file in the future.
                            if curl not in ok_ip_save_list:
                                count_ip += 1
                                ok_ip_save_list.append(curl)

                if save_ok_proxies:
                    if len(ok_ip_save_list) > number_of_save_proxies:
                        ok_ip_save_list = random.sample(ok_ip_save_list, number_of_save_proxies)
                    File.save_records_list(ok_file, ok_ip_save_list, overwrite=True, exit_all=False)

            if not len(ok_ip_save_list):
                again = True
                message = "Proxy couldn't get. Trying again..."
                Progress.exit_app(message=message, exit_all=False)
                continue

            if get_random:
                curl = random.choice(ok_ip_save_list)
            else:
                # Remaining calculated to get a proxy from our list, from LAST to FIRST.
                remaining = count_loop % len(ok_ip_save_list)
                remaining = len(ok_ip_save_list) - remaining
                if remaining >= len(ok_ip_save_list):
                    remaining = 0

                curl = ok_ip_save_list[remaining]
            curl = curl.replace(' ', '')
            curl = curl.replace('\n', '')

            proxy_decide = {}
            if for_https:
                proxy_decide['https'] = curl
            else:
                proxy_decide['http'] = curl

            if save_false_proxies:
                if curl in error_ip_list:
                    File.write_ok_and_false_proxy(curl, error_file=error_file, ok_file=ok_file)
                    again = True
                    continue

            if run_test:
                try:
                    if check_internet:
                        internet_connection(timeout=test_timeout, reload_time=30, wait_for_network=True, sound_error=sound_error)

                    response = requests.get(url, proxies=proxy_decide, timeout=test_timeout, stream=True, headers=test_header)
                    if test_url:
                        # if any url overwritten on def, just check the status code.
                        if response.status_code != 200:
                            raise Exception
                    else:
                        response = response.json()
                        if response == {}:
                            raise Exception
                    if save_ok_proxies:
                        File.save_records_list(ok_file, ok_ip_save_list, overwrite=True, exit_all=False)
                except Exception as e:
                    message = "Proxy doesn't work. Next proxy is testing...\n" \
                              "Proxy: %s" % (curl)
                    if not get_random:
                        message += '\tProxy Number: %s' % remaining
                    if allow_print:
                        print(message)
                        print()
                    again = True
                    if save_false_proxies:
                        File.write_ok_and_false_proxy(curl, error_file=error_file, ok_file=ok_file)
                    continue

            ip_port = curl.split('//')[-1]
            if selenium:
                proxy_decide = '--proxy-server=%s' % (ip_port)
            else:
                # proxy_decide defined above.
                pass

            if allow_print:
                if get_random:
                    print("Proxy activated.\nProxy: %s" % (curl))
                else:
                    print("Proxy activated. Proxy Number: %s.\nProxy: %s" % (count_loop, curl))

    if allow_print:
        print()
    if get_random:
        return proxy_decide, curl
    else:
        return count_loop, proxy_decide, curl
# USAGE GET PROXY -----------------------
"""
proxy_decide, curl = get_proxy(selenium=False, get_random=True, run_test=False)  # OPTION 1
count_loop += 1  # OPTION 2
count_loop, proxy_decide, curl = get_proxy(selenium=False, get_random=False, count_loop=count_loop, run_test=False)  # OPTION 2
response = requests.get(
    url,
    headers={},
    stream=True,
    proxies=proxy_decide,
    timeout=5,
)
"""
# USAGE GET PROXY -----------------------

def internet_connection(timeout=4, reload_time=30, wait_for_network=True, sound_error=True):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
    header = {"User-Agent": user_agent}

    url_list = [
        # 'https://api.myip.com/',
        # 'https://api.ipify.org/',
        'https://www.yahoo.com/',
        'https://www.bing.com/',
        'https://www.google.com/',
        'https://www.amazon.com/',
        'https://www.amazon.com.tr/',
        'https://www.microsoft.com/',
        'https://www.apple.com/',
    ]

    message_pasted = False
    length_of_last_message = 0
    length_of_last_message_MAX = 0
    while True:
        try:
            url = random.choice(url_list)

            network = True
            response = requests.get(url, timeout=timeout, headers=header)

            if response.status_code != 200:
                raise Exception
        except:
            # There is no internet connection.
            network = False

        if not wait_for_network and network:
            # if there is internet connection OR def overwritten to not wait for network, RETURN
            return network

        if network:
            if message_pasted:
                # If there was "False network" and 'count down' printed,
                # paste space as much as pasted text before.
                # Because after pyinstaller execution, print flush, prints in bad view.
                message = 'Connection established.'
                length_of_new_message = len(message)
                if length_of_last_message - length_of_new_message > 0:
                    message = message + ' ' * (length_of_last_message_MAX - length_of_new_message)
                print("\r%s" % message, flush=True, end="")
                print()
                print()
                print('-' * 40)
                print()
            # Continue to run main program (RETURN DEF)
            break
        else:
            if not message_pasted:
                print()
                print('-' * 10)
                print()
                if sound_error:
                    Progress.sound_notify()
                message_pasted = True
                print(url)  # DEBUG

            now = time.time()
            time.sleep(0.01)
            message = ''
            while time.time() - now < reload_time:
                remaining_time = int(reload_time - (time.time() - now))
                net_time_string = Progress.time_definition(remaining_time)
                message = '--> Error on internet connection. Trying again in %s.' % net_time_string
                print("\r%s" % message, flush=True, end="")
                time.sleep(1)
            length_of_last_message = len(message)
            if length_of_last_message_MAX < length_of_last_message:
                length_of_last_message_MAX = length_of_last_message


