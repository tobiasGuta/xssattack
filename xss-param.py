import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import signal
import sys
from rich.console import Console
from rich.table import Table

art = r'''
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

# Initialize rich console
console = Console()

# Global list to store triggered payload URLs
triggered_payloads = []

def setup_browser():
    # Set up the WebDriver using the webdriver-manager
    options = webdriver.ChromeOptions()
    # Add any desired options like headless mode if needed
    # options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def detect_alert(driver, url, param, payload, output_file=None):
    # Insert the payload into the specified parameter in the URL
    test_url = f"{url}?{param}={payload}"
    driver.get(test_url)
    
    try:
        # Wait for an alert to be present, up to 5 seconds
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        
        # If an alert is found, handle it
        alert = Alert(driver)
        console.print(f"[bold green]ALERT:[/] Alert detected with payload: [yellow]{payload}[/] for parameter: {param}")
        alert.accept()  # You can also dismiss or perform other actions if needed
        console.print(f"[bold green]ALERT:[/] Alert accepted!")
        
        # Add the triggered payload URL to the list
        triggered_payloads.append(test_url)
        
        # Save the triggered payload URL to the output file if specified
        if output_file:
            with open(output_file, 'a') as f:
                f.write(test_url + '\n')
        return "Triggered"
    
    except Exception as e:
        console.print(f"[bold yellow]INFO:[/] No alert detected with payload: [yellow]{payload}[/] for parameter: {param}.")
        return "Not Triggered"

def signal_handler(sig, frame):
    console.print(f"\n[bold red]ERROR:[/] Program interrupted. Exiting gracefully...")
    sys.exit(0)

def main():
    # Set up signal handling for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Detect and handle JavaScript alerts on a webpage.")
    parser.add_argument("url", type=str, help="The URL of the target webpage.")
    parser.add_argument("-f", "--file", type=str, required=True, help="The file containing payloads to test.")
    parser.add_argument("-p", "--param", type=str, required=True, help="The name of the URL parameter to insert payloads into.")
    parser.add_argument("-n", "--num_payloads", type=int, default=None, help="Number of payloads to send from the list.")
    parser.add_argument("-o", "--output", type=str, help="File to save the output of triggered payloads.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Read payloads from the file
    try:
        with open(args.file, "r") as file:
            payloads = file.readlines()
    except FileNotFoundError:
        console.print(f"[bold red]ERROR:[/] Payload file not found!")
        sys.exit(1)
    
    # Limit the number of payloads to send if specified
    if args.num_payloads:
        payloads = payloads[:args.num_payloads]
    
    # Initialize the browser
    driver = setup_browser()
    
    # Display header for results table
    table = Table(title="Triggered Payloads")
    table.add_column("No.", justify="right", style="bold")
    table.add_column("Payload", style="dim", width=40)
    table.add_column("URL", justify="center")
    table.add_column("Status", justify="center", style="bold green")
    
    # Test each payload
    for i, payload in enumerate(payloads):
        payload = payload.strip()  # Remove leading/trailing whitespace
        status = detect_alert(driver, args.url, args.param, payload, args.output)
        
        # Add triggered payload to table
        if f"{args.url}?{args.param}={payload}" in triggered_payloads:
            table.add_row(str(i + 1), payload, f"{args.url}?{args.param}={payload}", "Triggered")
        else:
            table.add_row(str(i + 1), payload, f"{args.url}?{args.param}={payload}", "Not Triggered")
    
    driver.quit()
    
    # Show the final results table in the console
    console.print(table)

if __name__ == "__main__":
    main()
