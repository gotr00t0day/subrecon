from fake_useragent import UserAgent
from colorama import Fore, Back, Style
import subprocess
import requests
import time
import socket

#SubRec0n v1.0 by c0deninja

banner = """
            ___.                       _______          
  ________ _\_ |_________   ____   ____ \   _  \   ____  
 /  ___/  |  \ __ \_  __ \_/ __ \_/ ___\/  /_\  \ /    \ 
 \___ \|  |  / \_\ \  | \/\  ___/\  \___\  \_/   \   |  \\
/____  >____/|___  /__|    \___  >\___  >\_____  /___|  /
     \/          \/            \/     \/       \/     \/  v1.0
                        by c0deninja

"""

print(Fore.CYAN + banner)

domain = input(Fore.WHITE + "Enter Domain: ")

def commands(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except:
        pass
    
print("\n")
print(Fore.CYAN + "Scanning for subdomains...\n")
time.sleep(2)

cmd = "subfinder -d {}".format(domain)
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
subfinderout, err = p.communicate()
subfinderout = subfinderout.decode()

with open('subdomains.txt', 'w') as subfinder:
    subfinder.writelines(subfinderout)

cmd = "amass enum -passive -d {}".format(domain)
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
amassout, err = p.communicate()
amassout = amassout.decode()

with open('subdomains.txt', 'a') as amass:
    amass.writelines(amassout)


print (Fore.WHITE + "probing subdomains...." + "\n")

with open('subdomains.txt', 'r') as f:
    subdomains = f.readlines()

gooddomains = []

def ipadd(subdomain):
    if "http" in subdomain:
        subdomain = subdomain.replace("http://", "")
    if "https" in subdomain:
        subdomain = subdomain.replace("https://", "")
    return socket.gethostbyname(subdomain)

# probing subdomains
for domains in subdomains:
    try:
        domains = domains.strip()
        https = "https://" + domains
        http = "http://" + domains
        ua = UserAgent()
        header = {'User-Agent':str(ua.chrome)}     
        resphttp = requests.get(http, headers=header)
        resphttps = requests.get(https, headers=header)
        if resphttp.status_code == 200:
            print (Fore.GREEN + "{}: {}".format(http, ipadd(http)))
            gooddomains.append(http + "\n")
        if resphttps.status_code == 200:
            print (Fore.GREEN + "{}: {}".format(https, ipadd(https)))
            gooddomains.append(https + "\n")
    except:
        print(Fore.RED + "{}".format(domains))

with open("goodsubs.txt", "w") as g:
    g.writelines(gooddomains)
