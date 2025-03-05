from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import urllib.parse
import concurrent.futures
import random
import logging

art = r'''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣤⡤⣤⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠉⠀⠀⠀⠀⠀⠀⠀⠘⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡟⠀⣀⠀⠀⠀⠀⠀⠀⣀⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠁⠀⠛⠀⠀⠀⠀⠀⠀⠛⠀⠀⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣻⣋⠀⠿⠿⠿⠀⠀⠀⠀⠿⠿⠿⠀⢘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣟⠀⠀⣿⠀⠀⠀⠀⠀⠀⣿⠀⠀⢘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⣷⣿⣗⠀⠀⣿⠀⠀⠀⠀⠀⠀⣿⠀⠀⢘⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣟⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⣯⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣯⣷⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⡿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡺⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣯⣿⡄⠀⠘⠻⠿⠿⠿⠃⠀⣐⣟⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣷⣿⡿⡿⣿⣽⣟⢷⣄⣀⣀⣀⣀⣠⣾⢿⣿⣟⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⡿⣻⣿⡿⣿⣯⡯⣿⣿⣶⣷⣾⣾⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⣿⣿⣿⣿⣿⣷⣿⣼⣿⣟⣿⣧⣿⣿⣿⣿⣿⣿⣷⣗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡟⣿⣿⡾⣿⣷⣿⣛⣻⣷⡟⡯⣷⣮⣟⣿⣽⢿⣻⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣯⣟⣟⣛⣞⡻⣿⣿⠽⡼⢟⡷⡗⣿⡎⠿⡿⣽⣏⣾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⣽⡡⡧⢅⢟⢇⡏⢭⠳⡃⣙⢇⣮⡗⡗⡏⠿⣗⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⣯⡏⠝⣡⣋⠠⠨⣇⡯⠱⡙⠁⣍⢬⡺⡏⡕⣧⠉⡬⣽⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣃⡂⠃⠘⠀⡏⠡⣎⡁⠂⠀⢼⠄⠂⠀⠃⠛⡁⠉⠁⡿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠉⠀⠀⠀⠀⠀⠈⠑⡇⠀⠀⠘⠀⠃⠀⠁⣛⠃⠀⠀⠧⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⠀⠀⠀⠹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
             __  ______ ____  
             \ \/ / ___/ ___| 
              \  /\___ \___ \ 
              /  \ ___) |__) |
             /_/\_\____/____/ 
                  ⠀⠀⠀⠀⠀⠀⠀
'''

print(art)

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ANSI Colors for CLI Output
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'


def load_payloads(file_path):
    """Load payloads from a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        logging.error(f"{RED}File '{file_path}' not found.{RESET}")
        return []


def escape_payload(payload):
    """Escape special characters in payloads for safe injection."""
    return urllib.parse.quote(payload)


def check_alert(driver, wait):
    """Check for JavaScript alert pop-ups."""
    try:
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()  # Close the alert
        return alert_text
    except:
        return None


def test_payload(payload, base_url, param):
    """Test a single payload for XSS vulnerabilities."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU for stability
    options.add_argument('--no-sandbox')  # Bypass OS security restrictions
    options.add_argument('--disable-dev-shm-usage')  # Prevent shared memory issues

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 5)

    result = {"payload": payload, "alert_text": None}

    try:
        # Properly encode the parameter into the URL
        parsed_url = urllib.parse.urlparse(base_url)
        query_params = dict(urllib.parse.parse_qsl(parsed_url.query))
        query_params[param] = payload
        test_url = parsed_url._replace(query=urllib.parse.urlencode(query_params)).geturl()

        driver.get(test_url)

        # Check if an alert popped up
        alert_text = check_alert(driver, wait)
        if alert_text:
            result['alert_text'] = alert_text
            logging.info(f"{GREEN}[ALERT] XSS detected with payload: {payload}{RESET}")
        else:
            logging.info(f"{RED}[NO ALERT] No XSS detected with payload: {payload}{RESET}")

    except Exception as e:
        logging.error(f"{RED}[ERROR] Payload: {payload} | Exception: {e}{RESET}")
    finally:
        driver.quit()
        if result["alert_text"]:
            return result  # Return the result when alert is triggered
        else:
            return None  # Return None if no alert was triggered


def save_triggered_payloads(results, output_file, base_url, param):
    """Save the triggered payloads to a file in the desired format."""
    if results:
        with open(output_file, 'w') as file:
            for result in results:
                # Properly encode the payload and inject it into the base URL
                parsed_url = urllib.parse.urlparse(base_url)
                query_params = dict(urllib.parse.parse_qsl(parsed_url.query))
                query_params[param] = result['payload']
                test_url = parsed_url._replace(query=urllib.parse.urlencode(query_params)).geturl()
                file.write(f"{test_url}\n")
        logging.info(f"Triggered payloads saved to: {output_file}")
    else:
        logging.info("No payloads triggered alerts, nothing to save.")


def main():
    parser = argparse.ArgumentParser(description='XSS Testing Tool with Alert Detection')
    parser.add_argument('-u', '--url', required=True, help='Target URL (use [PARAM] as a placeholder)')
    parser.add_argument('-p', '--param', required=True, help='Parameter name to inject payloads')
    parser.add_argument('-f', '--file', required=True, help='File containing payloads')
    parser.add_argument('-n', '--number', type=int, default=10, help='Number of payloads to test')
    parser.add_argument('-t', '--trigger', default='triggered_payloads.txt', help='File to save triggered payloads')

    args = parser.parse_args()
    base_url = args.url
    param = args.param
    triggered_file = args.trigger

    # Load and select random payloads
    payloads = load_payloads(args.file)
    if not payloads:
        logging.error("No payloads loaded. Exiting.")
        return

    payloads_to_test = random.sample(payloads, min(args.number, len(payloads)))

    # Run tests in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(test_payload, payloads_to_test, [base_url] * len(payloads_to_test), [param] * len(payloads_to_test)))

    # Filter out None values from results
    filtered_results = [result for result in results if result is not None]

    # Save triggered payloads
    save_triggered_payloads(filtered_results, triggered_file, base_url, param)


if __name__ == "__main__":
    main()
