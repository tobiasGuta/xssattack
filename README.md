# xssattack

This Python tool is designed to test web applications for Cross-Site Scripting (XSS) vulnerabilities by injecting payloads into specified URL parameters and detecting JavaScript alerts. It leverages the Selenium library for browser automation, uses webdriver-manager for ChromeDriver management, and supports concurrent execution for efficiency. Results are compiled into an HTML report and automatically opened in Firefox.

![xss](https://github.com/user-attachments/assets/518568e3-875d-4215-9999-46653cf54974)


# Features

Automated XSS Testing: Automatically injects payloads into specified URL parameters and checks for JavaScript alerts.
Headless Browser Execution: Uses a headless Chrome browser for testing, which allows for running tests without a visible UI.
Concurrent Execution: Tests are performed in parallel using Python’s concurrent.futures to speed up the process.
Custom Payloads: Supports custom payloads loaded from a file.
HTML Report Generation: Compiles the results into an HTML report with a styled table that lists payloads that triggered alerts.
Automatic Report Opening: The generated report is automatically opened in Firefox for quick review.

# Usage

The tool is executed from the command line with several arguments:

    python xss_tester.py -u <URL> -p <PARAM> -f <PAYLOAD_FILE> [-n <NUMBER>] [-o <OUTPUT_FILE>]
Arguments:

    -u, --url (Required): The URL to test, ending with a parameter placeholder (e.g., http://example.com/page?param=).
    -p, --param (Required): The name of the parameter to inject payloads into (e.g., search).
    -f, --file (Required): Path to a file containing custom payloads (one per line).
    -n, --number (Optional): Number of random payloads to test. Defaults to 10.
    -o, --output (Optional): The name of the output HTML report file. Defaults to report.html.

Example

To test a URL with a parameter and a payload file, and generate a report:

    python xss_tester.py -u http://example.com/search -p q -f payloads.txt -n 5 -o xss_report.html

Dependencies

    Selenium
    WebDriver Manager
    argparse
    urllib.parse
    concurrent.futures
    random
    html
    webbrowser
    os

Ensure you have these dependencies installed and configured for the tool to function correctly. The webdriver-manager library automatically handles ChromeDriver downloads and updates, so no manual setup is required.
Note

The script assumes that Firefox is installed at a default location on the system. Adjust the path to the Firefox executable if necessary for different environments.
