from colorama import Style
import discord, datetime, time, requests, json, threading, os, random, httpx, sys
import tls_client
from pathlib import Path
from threading import Thread
import hashlib

config = json.load(open("config.json", encoding="utf-8")) 


class Fore:
    BLACK  = '\033[30m'
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    BLUE   = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN   = '\033[36m'
    WHITE  = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET  = '\033[0m'
    
os.system(f"title boost tool by discord.gg/9cloud by Sag3ata#0001")    
fingerprints = json.load(open("fingerprints.json", encoding="utf-8"))


client_identifiers = ['safari_ios_16_0', 'safari_ios_15_6', 'safari_ios_15_5', 'safari_16_0', 'safari_15_6_1', 'safari_15_3', 'opera_90', 'opera_89', 'firefox_104', 'firefox_102']


class variables:
    joins = 0; boosts_done = 0; success_tokens = []; failed_tokens = []




 
def checkEmpty(filename): #checks if the file passed is empty or not
    mypath = Path(filename)
 
    if mypath.stat().st_size == 0:
        return True
    else:
        return False
    
    
def validateInvite(invite:str): #checks if the invite passed is valid or not
    client = httpx.Client()
    if 'type' in client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text:
        return True
    else:
        return False 


def sprint(message, type):
    if type == True:
        print(f"{Style.BRIGHT}{Fore.MAGENTA}[+]{Style.BRIGHT} {message}{Fore.RESET}{Style.RESET_ALL}")
    if type == False:
        print(f"{Style.BRIGHT}{Fore.MAGENTA}[-]{Style.BRIGHT} {message}{Fore.RESET}{Style.RESET_ALL}")
    if type == "blue":
        print(f"{Style.BRIGHT}{Fore.MAGENTA}{message}{Fore.RESET}{Style.RESET_ALL}")    
        

def get_all_tokens(filename:str): #returns all tokens in a file as token from email:password:token
    all_tokens = []
    for j in open(filename, "r").read().splitlines():
        if ":" in j:
            j = j.split(":")[2]
            all_tokens.append(j)
        else:
            all_tokens.append(j)
 
    return all_tokens



def remove(token: str, filename:str):
    tokens = get_all_tokens(filename)
    tokens.pop(tokens.index(token))
    f = open(filename, "w")
    
    for l in tokens:
        f.write(f"{l}\n")
        
    f.close()
            
        
        
#get proxy
def getproxy():
    try:
        proxy = random.choice(open("input/proxies.txt", "r").read().splitlines())
        return {'http': f'http://{proxy}'}
    except Exception as e:
        #sprint(f"{str(e).capitalize()} | Function: GetProxy, Retrying", False)
        pass
    
    
def get_fingerprint(thread):
    try:
        fingerprint = httpx.get(f"https://discord.com/api/v10/experiments", proxies =  {'http://': f'http://{random.choice(open("input/proxies.txt", "r").read().splitlines())}', 'https://': f'http://{random.choice(open("input/proxies.txt", "r").read().splitlines())}'} if config['proxyless'] != True else None)
        return fingerprint.json()['fingerprint']
    except Exception as e:
        #sprint(f"[{thread}] {str(e).capitalize()} | Function: Get_Fingerprint, Retrying", False)
        get_fingerprint(thread)


def get_cookies(x, useragent, thread):
    try:
        response = httpx.get('https://discord.com/api/v10/experiments', headers = {'accept': '*/*','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','content-type': 'application/json','origin': 'https://discord.com','referer':'https://discord.com','sec-ch-ua': f'"Google Chrome";v="108", "Chromium";v="108", "Not=A?Brand";v="8"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': useragent, 'x-debug-options': 'bugReporterEnabled','x-discord-locale': 'en-US','x-super-properties': x}, proxies = {'http://': f'http://{random.choice(open("input/proxies.txt", "r").read().splitlines())}', 'https://': f'http://{random.choice(open("input/proxies.txt", "r").read().splitlines())}'} if config['proxyless'] != True else None)
        cookie = f"locale=en; __dcfduid={response.cookies.get('__dcfduid')}; __sdcfduid={response.cookies.get('__sdcfduid')}; __cfruid={response.cookies.get('__cfruid')}"
        return cookie
    except Exception as e:
        #sprint(f"[{thread}] {str(e).capitalize()} | Function: Get_Cookies, Retrying", False)
        get_cookies(x, useragent, thread)


#get headers
def get_headers(token,thread):
    x = fingerprints[random.randint(0, (len(fingerprints)-1))]['x-super-properties']
    useragent = fingerprints[random.randint(0, (len(fingerprints)-1))]['useragent']
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer':'https://discord.com',
        'sec-ch-ua': f'"Google Chrome";v="108", "Chromium";v="108", "Not=A?Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'cookie': get_cookies(x, useragent, thread),
        'sec-fetch-site': 'same-origin',
        'user-agent': useragent,
        'x-context-properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjY3OTg3NTk0NjU5NzA1NjY4MyIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiIxMDM1ODkyMzI4ODg5NTk0MDM2IiwibG9jYXRpb25fY2hhbm5lbF90eXBlIjowfQ==',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-super-properties': x,
        'fingerprint': get_fingerprint(thread)
        
        }

    return headers, useragent
    
    
#solve captcha
def get_captcha_key(rqdata: str, site_key: str, websiteURL: str, useragent: str):

    task_payload = {
        'clientKey': config['capmonster_key'],
        'task': {
            "type"             :"HCaptchaTaskProxyless",
            "isInvisible"      : True,
            "data"             : rqdata,
            "websiteURL"       : websiteURL,
            "websiteKey"       : site_key,
            "userAgent"        : useragent
                        }
    }
    key = None
    with httpx.Client(headers={'content-type': 'application/json', 'accept': 'application/json'},
                    timeout=30) as client:   
        task_id = client.post(f'https://api.capmonster.cloud/createTask', json=task_payload).json()['taskId']
        get_task_payload = {
            'clientKey': config['capmonster_key'],
            'taskId': task_id,
        }
        

        while key is None:
            response = client.post("https://api.capmonster.cloud/getTaskResult", json = get_task_payload).json()
            if response['status'] == "ready":
                key = response["solution"]["gRecaptchaResponse"]
            else:
                time.sleep(1)
            
    return key
    

#join server
def join_server(session, headers, useragent, invite, token, thread):
    join_outcome = False
    guild_id = 0
    try:
        for i in range(10):
            response = session.post(f'https://discord.com/api/v9/invites/{invite}', json={}, headers = headers)
            if response.status_code == 429:
                sprint(f"[{thread}] You are being rate limited. Sleeping for 5 seconds.", False)
                time.sleep(5)
                join_server(session, headers, useragent, invite, token)
                
            elif response.status_code in [200, 204]:
                #sprint(f"[{thread}] Joined without Captcha : {token}", True)
                join_outcome = True
                guild_id = response.json()["guild"]["id"]
                break
                #variables.joins += 1
            elif "captcha_rqdata" in response.text:
                #{'captcha_key': ['You need to update your app to join this server.'], 'captcha_sitekey': 'a9b5fb07-92ff-493f-86fe-352a2803b3df', 'captcha_service': 'hcaptcha', 'captcha_rqdata': '6x2V9nU0sF4schdwvU80ptu4CQnFEJQz1cA0pvoTzBbkXzGPoJLljDVNvlJBWFUm5yqj4p83buOfIcHKSIGqDlARNU0/ik6Xp5dC3+xbEQvsxT1juCKbLB4mAlDR4UJOKwO7UKbW35kXxtP8HLJ2nusPOjZnGtlDKI0R5f85', 'captcha_rqtoken': 'InZ4akJpMzBtS2Y0SVlsSEIzTTE3Q1ArTzA5VlQrM1dSOFVUc3RBUTJkS0JTUC9UUG90TUU2TzBIUGtZQkhLd0lsQnFJZUE9PXA1WnptRnJLME1CMDlQaHgi.Y73eww.S3g5RodcfWcgWI7MLihE0lkgf4A'}
                sprint(f"[{thread}] Captcha Detected: {token}", False)
                r = response.json()
                solution = get_captcha_key(rqdata = r['captcha_rqdata'], site_key = r['captcha_sitekey'], websiteURL = "https://discord.com", useragent = useragent)
                #sprint(f"[{thread}] Solution: {solution[:60]}...", True)
                response = session.post(f'https://discord.com/api/v9/invites/{invite}', json={'captcha_key': solution,'captcha_rqtoken': r['captcha_rqtoken']}, headers = headers)
                if response.status_code in [200, 204]:
                    #sprint(f"[{thread}] Joined with Captcha: {token}", True)
                    join_outcome = True
                    guild_id = response.json()["guild"]["id"]
                    break
                    #variables.joins += 1
                    
        return join_outcome, guild_id

            
    except Exception as e:
        #sprint(f"[{thread}] {str(e).capitalize()} | Function: Join, Retrying", False)
        join_server(session, headers, useragent, invite, token, thread)
        
        
#boost 1x
def put_boost(session, headers, guild_id, boost_id):
    try:
        payload = {"user_premium_guild_subscription_slot_ids": [boost_id]}
        boosted = session.put(f"https://discord.com/api/v9/guilds/{guild_id}/premium/subscriptions", json=payload, headers=headers)
        if boosted.status_code == 201:
            return True
        elif 'Must wait for premium server subscription cooldown to expire' in boosted.text:
            return False
    except Exception as e:
        #sprint(f"[{thread}] {str(e).capitalize()} | Function: Put_Boost, Retrying", False)
        put_boost(session, headers, guild_id, boost_id)
    
    
def change_guild_name(session, headers, server_id, nick):
    try:
        jsonPayload = {"nick": nick}
        r = session.patch(f"https://discord.com/api/v9/guilds/{server_id}/members/@me", headers=headers, json=jsonPayload)
        if r.status_code == 200:
            return True
        else:
            return False
        
    except Exception as e:
        #sprint(f"[{thread}] {str(e).capitalize()} | Function: Change_Guild_Name, Retrying", False)
        change_guild_name(session, headers, server_id, nick)
    
    
#boost server
def boost_server(invite:str , months:int, token:str, thread:int, nick: str):
    if months == 1:
        filename = "input/1m_tokens.txt"
    if months == 3:
        filename = "input/3m_tokens.txt"
    
    try:
        session = tls_client.Session(ja3_string = fingerprints[random.randint(0, (len(fingerprints)-1))]['ja3'], client_identifier = random.choice(client_identifiers))
        if config['proxyless'] == False and len(open("input/proxies.txt", "r").readlines()) != 0:
            proxy = getproxy()
            session.proxies.update(proxy)

        headers, useragent = get_headers(token, thread)
        boost_data = session.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)

        if "401: Unauthorized" in boost_data.text:
            sprint(f"[{thread}] INVALID: {token}", False)
            variables.failed_tokens.append(token)
            remove(token, filename)
            
        if "You need to verify your account in order to perform this action." in boost_data.text:
            sprint(f"[{thread}] LOCKED: {token}", False)
            variables.failed_tokens.append(token)
            remove(token, filename)
            
        if boost_data.status_code == 200:
            if len(boost_data.json()) != 0:
                join_outcome, guild_id = join_server(session, headers, useragent, invite, token, thread)
                if join_outcome:
                    sprint(f"[{thread}] JOINED: {token}", True)
                    for boost in boost_data.json():
                        boost_id = boost["id"]
                        boosted = put_boost(session, headers, guild_id, boost_id)
                        if boosted:
                            sprint(f"[{thread}] BOOSTED: {token}", True)
                            variables.boosts_done += 1
                            if token not in variables.success_tokens:
                                variables.success_tokens.append(token)    
                        else:
                            sprint(f"[{thread}] ERROR BOOSTING: {token}", False)
                            if token not in variables.failed_tokens:
                                open("error_boosting.txt", "a").write(f"\n{token}")
                                variables.failed_tokens.append(token)
                    remove(token, filename)

                    if config["change_server_nick"]:
                        changed = change_guild_name(session, headers, guild_id, nick)
                        if changed:
                            sprint(f"[{thread}] RENAMED: {token}", True)
                        else:
                            sprint(f"[{thread}] ERROR RENAMING: {token}", False)
                else:
                    sprint(f"[{thread}] ERROR JOINING: {token}", False)
                    open("error_joining.txt", "a").write(f"\n{token}")
                    remove(token, filename)
                    variables.failed_tokens.append(token)
            else:
                remove(token, filename)
                sprint(f"[{thread}] NO NITRO: {token}", False)
                variables.failed_tokens.append(token)
                                        
    except Exception as e:
        #sprint(f"[{thread}] {str(e).capitalize()} | Function: Boost_Server, Retrying", False)
        boost_server(invite, months, token, thread, nick)


def thread_boost(invite, amount, months, nick):
    variables.boosts_done = 0
    variables.success_tokens = []
    variables.failed_tokens = []
    
    if months == 1:
        filename = "input/1m_tokens.txt"
    if months == 3:
        filename = "input/3m_tokens.txt"
    
    if validateInvite(invite) == False:
        sprint(f"The invite received is invalid.", False)
        return False
        
    while variables.boosts_done != amount:
        print()
        tokens = get_all_tokens(filename)
        
        if variables.boosts_done % 2 != 0:
            variables.boosts_done -= 1
            
        numTokens = int((amount - variables.boosts_done)/2)
        if len(tokens) == 0 or len(tokens) < numTokens:
            sprint(f"Not enough {months} month tokens in stock to complete the request", False)
            return False
        
        else:
            threads = []
            for i in range(numTokens):
                token = tokens[i]
                thread = i+1
                t = threading.Thread(target=boost_server, args=(invite, months, token, thread, nick))
                t.daemon = True
                threads.append(t)
                
            for i in range(numTokens):
                sprint(f"Processing....\n", True)
                threads[i].start()
            print()
                
            for i in range(numTokens):
                threads[i].join()

            
    return True
    



print(f'''{Style.BRIGHT}{Fore.MAGENTA}
                  
   




███████████████████████████████████████████████████████████████████████████████████████████
█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░█████████░░░░░░░░░░░░░░█░░░░░░██░░░░░░█░░░░░░░░░░░░███
█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░█████████░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀░░░░█
█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░░░█░░▄▀░░█████████░░▄▀░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░▄▀▄▀░░█
█░░▄▀░░██░░▄▀░░█░░▄▀░░█████████░░▄▀░░█████████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█
█░░▄▀░░░░░░▄▀░░█░░▄▀░░█████████░░▄▀░░█████████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█
█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░█████████░░▄▀░░█████████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█
█░░░░░░░░░░▄▀░░█░░▄▀░░█████████░░▄▀░░█████████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█
█████████░░▄▀░░█░░▄▀░░█████████░░▄▀░░█████████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█
█░░░░░░░░░░▄▀░░█░░▄▀░░░░░░░░░░█░░▄▀░░░░░░░░░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░▄▀▄▀░░█
█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀░░░░█
█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░███
███████████████████████████████████████████████████████████████████████████████████████████
                                                                                              
                                                                                             





                                              
''')
print(f'''{Style.BRIGHT}{Fore.MAGENTA}                            Token Stock: {len(open('input/3m_tokens.txt', 'r').read().splitlines())} Boost Stock: {len(open('input/3m_tokens.txt', 'r').read().splitlines()) * 2}''' + Fore.RESET)	

def menu():
    invite = input(f"{Style.BRIGHT}{Fore.GREEN}[+]{Fore.MAGENTA} Invite: ")
    if ".gg/" in invite:
        invite = str(invite).split(".gg/")[1]
    elif "invite/" in invite:
        invite = str(invite).split("invite/")[1]
    if (
        '{"message": "Unknown Invite", "code": 10006}'
        in httpx.get(f"https://discord.com/api/v9/invites/{invite}").text):
        sprint("Invalid Invite Code", False)
        return

    try:
        months = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}[+]{Fore.MAGENTA} Months: "))
    except:
        sprint("Months can be 1 or 3 only", False)
        return
    if months != 1 and months != 3:
        sprint("Months can be 1 or 3 only", False)
        return

    try:
        amount = (input(f"{Style.BRIGHT}{Fore.MAGENTA}[+] {Fore.MAGENTA}Amount: "))
    except:
        sprint("Amount must be Even", False)
        return
    amount = int(amount)
    if amount % 2 != 0:
        sprint("Amount must be Even", False)
        return
    nick = input(f"{Style.BRIGHT}{Fore.MAGENTA}[+] {Fore.MAGENTA}Nickname: ")
    go = time.time()
    thread_boost(invite, amount, months, nick)
    end = time.time()
    time_went = round(end - go, 5)
    print()
    print(f"\n{Style.BRIGHT}{Fore.GREEN}Time Taken: {time_went} seconds\nSuccessful Boosts: {len(variables.success_tokens)*2}")
    print(f"{Style.BRIGHT}{Fore.MAGENTA}Failed Boosts: {len(variables.failed_tokens)*2}{Fore.RESET}")
	
menu()