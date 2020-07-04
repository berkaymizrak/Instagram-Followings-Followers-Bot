# Progress Functions
# Berkay MIZRAK
# www.BerkayMizrak.com
# www.DaktiNetwork.com

try:
    import time

    import winsound

    # pip install pywin32
    import win32com.client as wincl
except Exception as e:
    print()
    print(e)
    while True:
        input('\n! ! ERROR --> A module is not installed...')


def exit_app(e=None, message=None, sound=False, sound_times=0, exit_all=True):
    print()
    if exit_all:
        print('!' + '-!-!' * 20)
    else:
        print('-' * 40)
    print()
    if sound:
        if sound_times == 0:
            sound_notify()
        else:
            sound_notify_times(sound_times)

    if e and message:
        print('ERROR:')
        if str(e) != '':
            print(str(e))
        if str(message) != '':
            print(message)
    else:
        if e and str(e) != '':
            print('ERROR:')
            print(str(e))
        if message and str(message) != '':
            print(message)
    print()
    if exit_all:
        print('!' + '-!-!' * 20)
        while True:
            input()
    else:
        print('-' * 40)
        print()

def sound_notify(show_error=True):
    try:
        for i in range(0, 3):
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 750  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)

        for k in range(0, 3):
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 500  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
    except Exception as e:
        if show_error:
            print('Error on windows sound notification:')
            print(e)

def sound_notify_times(times=3, frequency=2500, duration=500, show_error=True):
    try:
        for k in range(0, times):
            frequency_sound = frequency  # Set Frequency To 2500 Hertz
            if times == 1:
                duration_sound = 750  # Set Duration To 1000 ms == 1 second
            else:
                duration_sound = duration  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency_sound, duration_sound)
    except Exception as e:
        if show_error:
            print('Error on windows sound notification:')
            print(e)

def speech_text(text, sound_notify_work=False, exit_all=False):
    try:
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak(text)
    except Exception as e:
        if sound_notify_work:
            sound_notify_times(times=1)
        message = '--> An error occurred while speeching text:\n' \
                  '"%s"' % text
        exit_app(e=e, message=message, exit_all=exit_all)

def progress(count, total, now, message='In progress...', ):
    remaining_time = time_definition(int((total / (count / (time.time() - now))) - (time.time() - now)))
    passed_time = time_definition(int(time.time() - now))
    print(
        "\r{} |{}{}| {}% | {} | {} left."
            .format(
            message,
            "█" * int(25 * count / total),
            " " * (25 - int(25 * count / total)),
            int(100 * count / total),
            passed_time,
            remaining_time
        ),
        flush=True,
        end=""
    )

def time_definition(time_input):
    try:
        time_input = int(time_input)
    except:
        pass
    if time_input >= 60 * 60 * 24:
        remaining = time_input % (60 * 60 * 24)
        day = int(time_input / (60 * 60 * 24))
        hour = int(remaining / (60 * 60))
        minute = int(int(remaining / 60) % 60)
        second = int(remaining % 60)

        if day > 99:
            final_time_string = '99+ day %s h %s min %s s' % (hour, minute, second)
        else:
            if not second:
                if not minute:
                    if not hour:
                        final_time_string = '%s day' % (day)
                    else:
                        final_time_string = '%s day %s h' % (day, hour)
                else:
                    final_time_string = '%s day %s h %s min' % (day, hour, minute)
            else:
                final_time_string = '%s day %s h %s min %s s' % (day, hour, minute, second)
    elif time_input >= 60 * 60:
        remaining = time_input % (60 * 60)
        hour = int(time_input / (60 * 60))
        minute = int(remaining / 60)
        second = int(remaining % 60)
        if not second:
            if not minute:
                final_time_string = '%s h' % (hour)
            else:
                final_time_string = '%s h %s min' % (hour, minute)
        else:
            final_time_string = '%s h %s min %s s' % (hour, minute, second)
    elif time_input >= 60:
        minute = int(time_input / 60)
        second = int(time_input % 60)
        if not second:
            final_time_string = '%s min' % (minute)
        else:
            final_time_string = '%s min %s s' % (minute, second)
    else:
        final_time_string = '%s s' % (time_input)
    return final_time_string

def count_down(second, message='Counting down.'):
    net_time = time_definition(second)

    now = time.time()
    wait = False
    time.sleep(0.01)
    while time.time() - now < second:
        if wait:
            time.sleep(1)
        wait = True
        progress(
            count=time.time() - now,
            total=second,
            now=now,
            message='%s (%s)' % (message, net_time)
        )

def count_forward(now, message='Waiting'):
    passed_time = time.time() - now

    passed_time_string = time_definition(passed_time)

    passed_time_rounded = round(passed_time * 2) / 2

    if passed_time_rounded % 2 == 0:
        icon = '|'
    elif passed_time_rounded % 2 == 0.5:
        icon = '/'
    elif passed_time_rounded % 2 == 1:
        icon = '-'
    elif passed_time_rounded % 2 == 1.5:
        icon = '\\'
    else:
        icon = '-'

    print(
        "\r{} | {}... ({})"
            .format(
            message,
            passed_time_string,
            icon,
        ),
        flush=True,
        end=""
    )
# USAGE OF COUNT FORWARD -------------------
"""
now = time.time()
while True:  # add condition here.
    Progress.count_forward(now=now, )

    time.sleep(0.5)
"""
# USAGE OF COUNT FORWARD -------------------

