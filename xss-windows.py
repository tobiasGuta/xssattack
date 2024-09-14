from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import argparse
import urllib.parse
import concurrent.futures
import random
import html  # Import the html module for escaping payloads
import os  # Import the os module for handling system paths
import subprocess  # Import subprocess for better command execution

# ANSI escape codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

# Shared list to store results
results = []

def load_payloads(file_path):
    """Load payloads from a file."""
    try:
        with open(file_path, 'r') as file:
            payloads = file.read().splitlines()
        return payloads
    except FileNotFoundError:
        print(f"{RED}Error: The file '{file_path}' was not found.{RESET}")
        return []

def escape_payload(payload):
    """Escape special characters in payloads."""
    return urllib.parse.quote(payload)

def check_alert(driver, wait):
    """Check for JavaScript alert."""
    try:
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()  # Accept the alert
        return alert_text
    except:
        return None

def test_payload(payload, url, param):
    """Test a single payload for XSS vulnerabilities."""
    
    # Suppress logging messages from Selenium and ChromeDriver
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--log-level=3')  # Suppress logs (only errors will be shown)
    
    # Suppress DevTools logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Create a service object and suppress the log file
    service = Service(ChromeDriverManager().install())
    service.log_path = os.devnull  # Redirect logs to null to suppress them

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 5)  # Shorter wait time for alerts

    result = {
        'payload': payload,
        'alert_text': None
    }

    try:
        # Prepare the URL by replacing the placeholder with the payload
        if param not in url:
            print(f"{RED}[ERROR] Parameter '{param}' not found in URL.{RESET}")
            return

        # Inject payload into the URL parameter
        encoded_payload = escape_payload(payload)
        test_url = url.replace(param, f"{param}={encoded_payload}")
        driver.get(test_url)

        # Check for alert
        alert_text = check_alert(driver, wait)
        if alert_text:
            result['alert_text'] = alert_text
            print(f"{GREEN}[ALERT] XSS vulnerability detected with payload: {payload}. Alert text: {alert_text}{RESET}")
        else:
            print(f"{RED}[NO ALERT] No XSS vulnerability detected with payload: {payload}{RESET}")

    except Exception as e:
        print(f"{RED}[ERROR] Error testing payload: {payload}. Exception: {e}{RESET}")
    finally:
        driver.quit()
        if result['alert_text']:
            results.append(result)

def generate_html_report(results, output_file):
    """Generate an HTML report from the results."""
    num_triggered = len(results)

    with open(output_file, 'w') as file:
        file.write("<html><head><title>XSS Testing Report</title>")
        file.write("<style>")
        file.write("body { font-family: Arial, sans-serif; background: #111; color: #0f0; margin: 0; padding: 0; text-align: center; }")
        file.write("h1 { color: #0f0; margin: 20px 0; }")
        file.write("table { width: 80%; border-collapse: collapse; margin: 20px auto; }")
        file.write("table, th, td { border: 1px solid #0f0; }")
        file.write("th, td { padding: 10px; text-align: left; }")
        file.write("th { background: #333; }")
        file.write("tr:nth-child(even) { background: #222; }")
        file.write("tr:nth-child(odd) { background: #111; }")
        file.write("</style>")
        file.write("</head><body>")
        file.write("<h1>XSS Report</h1>")
        file.write(f"<p>Payloads that triggered alerts: {num_triggered}</p>")

        if results:
            file.write("<table><tr><th>Payload</th><th>Alert Text</th></tr>")
            for result in results:
                payload_safe = html.escape(result['payload'])  # Escape the payload for safe HTML display
                alert_text_safe = html.escape(result['alert_text'])  # Escape the alert text for safe HTML display
                file.write(f"<tr><td>{payload_safe}</td><td>{alert_text_safe}</td></tr>")
            file.write("</table>")
        else:
            file.write("<p>No payloads triggered alerts.</p>")
        
        file.write("</body></html>")

def open_report_in_chrome(report_path):
    """Open the report in Google Chrome."""
    chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'  # Path to Chrome executable

    if not os.path.isfile(chrome_path):
        print(f"{RED}Google Chrome executable not found at {chrome_path}. Cannot open report.{RESET}")
        return
    
    # Get the absolute path of the report
    report_abs_path = os.path.abspath(report_path)

    if not os.path.isfile(report_abs_path):
        print(f"{RED}Report file not found at {report_abs_path}. Cannot open report.{RESET}")
        return
    
    try:
        subprocess.run([chrome_path, report_abs_path], check=True)
    except Exception as e:
        print(f"{RED}Failed to open report in Google Chrome. Exception: {e}{RESET}")

def main():
    parser = argparse.ArgumentParser(description='XSS Testing Tool with Alert Detection')
    parser.add_argument('-u', '--url', required=True, help='URL to test, ending with a parameter placeholder')
    parser.add_argument('-p', '--param', required=True, help='Parameter name to inject payload into')
    parser.add_argument('-f', '--file', required=True, help='File containing custom payloads')
    parser.add_argument('-n', '--number', type=int, default=10, help='Number of random payloads to test')
    parser.add_argument('-o', '--output', default='report.html', help='Output HTML report file name')

    args = parser.parse_args()
    test_url = args.url
    test_param = args.param
    num_payloads_to_test = args.number
    output_file = args.output

    # Load payloads from file
    payloads = load_payloads(args.file)
    if not payloads:
        print(f"{RED}No payloads to test. Exiting.{RESET}")
        return

    # Select a random sample of payloads
    payloads_to_test = random.sample(payloads, min(num_payloads_to_test, len(payloads)))

    # Use ThreadPoolExecutor to parallelize the testing
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(test_payload, payload, test_url, test_param) for payload in payloads_to_test]
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()  # To propagate exceptions if any

    # Generate the HTML report
    generate_html_report(results, output_file)
    print(f"Report generated: {output_file}")

    # Automatically open the report in Google Chrome
    open_report_in_chrome(output_file)

if __name__ == "__main__":
    main()
