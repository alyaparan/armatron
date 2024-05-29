import requests
import threading
import random
import logging
import argparse
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
from colorama import Fore

# Define default values
DEFAULT_URL = 'http://target-server.com'
DEFAULT_URI = '/'
DEFAULT_METHOD = 'POST'
DEFAULT_PARAMS = {}
DEFAULT_VALUES = {}
DEFAULT_COOKIES = {}
DEFAULT_LOG_FILE = 'exploit_log.txt'
DEFAULT_PAYLOAD_FILE = 'payloads.txt'
DEFAULT_USER_AGENTS_FILE = 'user-agents.txt'
DEFAULT_VERBOSE = False
DEFAULT_DEBUG = False

def load_file_lines(file_path):
    """Load lines from a file."""
    lines = []
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError as e:
        logging.error("File not found: {}".format(file_path))
    except Exception as e:
        logging.error("Error loading file {}: {}".format(file_path, e))
    return lines

def send_request(url, method, payload, user_agent, cookies, headers, auth, timeout=10, retries=3, verify_ssl=True, session=None):
    """Send a request with the specified method, payload, user-agent, cookies, headers, and authentication."""
    headers.update({'User-Agent': user_agent})
    
    session = session or requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        if auth:
            response = session.request(method, url, data=payload, headers=headers, cookies=cookies, auth=auth, timeout=timeout, verify=verify_ssl)
        else:
            response = session.request(method, url, data=payload, headers=headers, cookies=cookies, timeout=timeout, verify=verify_ssl)
        
        # Improved response handling
        if response.ok:
            response_text = response.text
            if len(response_text) > 1000:
                response_text = response_text[:1000] + '...'
                
            logging.info("Request to {} successful. Status code: {}. Response body: {}".format(url, response.status_code, response_text))
        else:
            logging.error("Request to {} failed. Status code: {}".format(url, response.status_code))
            
        return response
    except requests.exceptions.RequestException as e:
        logging.error("Error sending request: {}".format(e))
        return None

def exploit_single(target_url, uri, method, params, values, cookies, payload, user_agent, headers, auth, timeout=10, retries=3, verify_ssl=True, verbose=False, session=None):
    """Exploit a single target with the specified parameters."""
    url = target_url + uri
    try:
        response = send_request(url, method, {param: value for param, value in zip(params, values)}, user_agent, cookies, headers, auth, timeout, retries, verify_ssl, session)
        if response:
            if verbose:
                logging.info("Payload: {}, User-Agent: {}, Cookies: {}, Status Code: {}, Headers: {}, Body: {}".format(
                    payload, user_agent, cookies, response.status_code, response.headers, response.text
                ))
            else:
                logging.info("Exploited {} with {} and got status code {}".format(url, payload, response.status_code))
    except Exception as e:
        logging.error("Error exploiting {}: {}".format(url, e))

def exploit(target_url, uri, method, params, values, cookies, payloads, user_agents, headers, auth, timeout=10, retries=3, verify_ssl=True, verbose=False, debug=False, concurrency=10, rate_limit=0):
    """Exploit the target with the specified parameters."""
    logging.basicConfig(filename=DEFAULT_LOG_FILE, level=logging.INFO if not debug else logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    threads = []
    session = requests.Session()
    for _ in range(concurrency):  # Number of threads for concurrent requests
        for payload in payloads:
            for user_agent in user_agents:
                t = threading.Thread(target=exploit_single, args=(
                    target_url, uri, method, params, values, cookies, payload, user_agent, headers, auth, timeout, retries, verify_ssl, verbose, session
                ))
                threads.append(t)
                t.start()

                # Rate limiting
                if rate_limit > 0:
                    time.sleep(1 / rate_limit)

    for t in threads:
        t.join()
        
def main():

    # Define colors resembling the LGBT flag
    COLOR_RED = Fore.RED
    COLOR_ORANGE = Fore.YELLOW  # Replacing with yellow for orange color
    COLOR_YELLOW = Fore.LIGHTYELLOW_EX   # Using light yellow for yellow color
    COLOR_GREEN = Fore.GREEN
    COLOR_BLUE = Fore.BLUE
    COLOR_PURPLE = Fore.MAGENTA    # Using magenta for purple color

    # ASCII art with colored text
    ascii_art = """
     ..                                                                {}s                                           
  :**888H: `: .xH""                                                   {}8                                           
 X   `8888k XX888       .u    .      ..    .     :                   {}88       .u    .          u.      u.    u.   
'8hx  48888 ?8888     .d88B :@8c   .888: x888  x888.        u       {}888ooo  .d88B :@8c   ...ue888b   x@88k u@88c. 
'8888 '8888 `8888    ="8888f8888r ~`8888~'888X`?888f`    us888u.  -*8888888 ="8888f8888r  888R Y888r ^"8888""8888" 
 %888>'8888  8888      4888>'88"    X888  888X '888>  .@88 "8888"   8888      4888>'88"   888R I888>   8888  888R  
   "8 '888"  8888      4888> '      X888  888X '888>  9888  9888    8888      4888> '     888R I888>   8888  888R  
  .-` X*"    8888      4888>        X888  888X '888>  9888  9888    8888      4888>       888R I888>   8888  888R  
    .xhx.    8888     .d888L .+     X888  888X '888>  9888  9888   .8888Lu=  .d888L .+   u8888cJ888    8888  888R  
  .H88888h.~`8888.>   ^"8888*"     "*88%""*88" '888!` 9888  9888   ^%888*    ^"8888*"     "*888*P"    "*88*" 8888" 
 .~  `%88!` '888*~       "Y"         `~    "    `"`   "888*""888"    'Y"        "Y"         'Y"         ""   'Y"   
       `"     ""                                       ^Y"   ^Y'                                                   
                                                                                                                   
                                                                                                                   
Developed by @alyaparan                                                                                                                   
Cyber Security Specialist | Cyber Criminal Enthusiast
Name: Alik Paranyan
Location: Armenia

Hacking into systems while sipping Armenian coffee and contemplating the mysteries of the universe, this individual explores the dark corners of the internet, delights in making firewalls blush, advocates for LGBT rights, and aims to make the cyber world safer, all while approaching cybersecurity with a mischievous flair, asserting, "It's not a bug; it's an undocumented feature!"

Disclaimer: The "Armatron" exploitation tool is for educational purposes only. Use it responsibly, and remember, with great power comes great cybersecurity responsibilities!

    """.format(COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_PURPLE)

    # Print the colored ASCII art
    print(ascii_art)

    """Main function to parse arguments and run the exploit."""
    parser = argparse.ArgumentParser(description="Powerful Exploit Script")
    parser.add_argument("--url", default=DEFAULT_URL, help="Target URL (default: {})".format(DEFAULT_URL))
    parser.add_argument("--uri", default=DEFAULT_URI, help="Target URI (default: {})".format(DEFAULT_URI))
    parser.add_argument("--method", default=DEFAULT_METHOD, choices=["GET", "POST", "PUT", "DELETE"], help="HTTP method to use (default: {})".format(DEFAULT_METHOD))
    parser.add_argument("--param", nargs='+', help="Parameters")
    parser.add_argument("--value", nargs='+', help="Values")
    parser.add_argument("--cookie", nargs='+', help="Cookies")
    parser.add_argument("--payload-file", default=DEFAULT_PAYLOAD_FILE,
                        help="File containing payloads (default: {})".format(DEFAULT_PAYLOAD_FILE))
    parser.add_argument("--user-agents-file", default=DEFAULT_USER_AGENTS_FILE,
                        help="File containing user agents (default: {})".format(DEFAULT_USER_AGENTS_FILE))
    parser.add_argument("--headers", nargs='+', help="Custom headers as key-value pairs separated by ':'")
    parser.add_argument("--proxy", help="Proxy server URL")
    parser.add_argument("--auth", nargs=2, metavar=('username', 'password'), help="HTTP basic authentication credentials")
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent threads for sending requests (default: 10)")
    parser.add_argument("--no-ssl-verify", action="store_false", dest="verify_ssl", help="Disable SSL certificate verification")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--rate-limit", type=int, default=0, help="Requests per second rate limit (default: 0, no limit)")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout for each request in seconds (default: 10)")
    parser.add_argument("--retries", type=int, default=3, help="Number of retries for failed requests (default: 3)")
    parser.add_argument("--output-file", help="Output file to save the results")
    args = parser.parse_args()

    if args.interactive:
        # Interactive mode
        target_url = input("Enter target URL (default: {}): ".format(DEFAULT_URL)) or DEFAULT_URL
        uri = input("Enter target URI (default: {}): ".format(DEFAULT_URI)) or DEFAULT_URI
        method = input("Enter HTTP method (default: {}): ".format(DEFAULT_METHOD)) or DEFAULT_METHOD
        param_str = input("Enter parameters separated by space (e.g., param1 param2): ")
        params = param_str.split() if param_str else []
        value_str = input("Enter values separated by space (e.g., value1 value2): ")
        values = value_str.split() if value_str else []
        cookie_str = input("Enter cookies separated by space (e.g., cookie1=value1 cookie2=value2): ")
        cookies = dict(item.split('=') for item in cookie_str.split()) if cookie_str else {}
        payload_file = input("Enter payload file (default: {}): ".format(DEFAULT_PAYLOAD_FILE)) or DEFAULT_PAYLOAD_FILE
        user_agents_file = input("Enter user agents file (default: {}): ".format(DEFAULT_USER_AGENTS_FILE)) or DEFAULT_USER_AGENTS_FILE
        header_str = input("Enter custom headers as key-value pairs separated by ':' (e.g., key1:value1 key2:value2): ")
        headers = dict(item.split(':') for item in header_str.split()) if header_str else {}
        proxy = input("Enter proxy server URL: ") or None
        auth_str = input("Enter username and password for HTTP basic authentication separated by space: ")
        auth = tuple(auth_str.split()) if auth_str else None
        verbose = input("Enable verbose mode? (y/n): ").lower() == 'y'
        debug = input("Enable debug mode? (y/n): ").lower() == 'y'
        concurrency = int(input("Enter number of concurrent threads (default: 10): ") or 10)
        verify_ssl = input("Enable SSL certificate verification? (y/n): ").lower() == 'y'
        rate_limit = int(input("Enter requests per second rate limit (default: 0, no limit): ") or 0)
        timeout = int(input("Enter timeout for each request in seconds (default: 10): ") or 10)
        retries = int(input("Enter number of retries for failed requests (default: 3): ") or 3)
        output_file = input("Enter output file to save the results: ")
    else:
        target_url = args.url
        uri = args.uri
        method = args.method
        params = args.param
        values = args.value
        cookies = args.cookie
        payload_file = args.payload_file
        user_agents_file = args.user_agents_file
        headers = args.headers
        proxy = args.proxy
        auth = args.auth
        verbose = args.verbose
        debug = args.debug
        concurrency = args.concurrency
        verify_ssl = args.verify_ssl
        rate_limit = args.rate_limit
        timeout = args.timeout
        retries = args.retries
        output_file = args.output_file

    # Validate inputs
    if not all([target_url.startswith('http://'), target_url.startswith('https://')]):
        logging.error("Invalid URL format. Please make sure the URL starts with 'http://' or 'https://'.")
        return
    if not method:
        logging.error("Invalid HTTP method specified.")
        return
    if not all(params) or not all(values):
        logging.error("Parameters and values must be provided in pairs.")
        return

    # Load payloads and user agents from files
    payloads = load_file_lines(payload_file)
    user_agents = load_file_lines(user_agents_file)

    # Configure proxy if provided
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    # Run the exploit
    exploit(target_url, uri, method, params, values, cookies, payloads, user_agents, headers, auth, timeout=timeout, retries=retries, verify_ssl=verify_ssl, verbose=verbose, debug=debug, concurrency=concurrency, rate_limit=rate_limit)

if __name__ == "__main__":
    main()
