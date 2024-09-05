# xssattack

This Python tool is designed to test web applications for Cross-Site Scripting (XSS) vulnerabilities by injecting payloads into specified URL parameters and detecting JavaScript alerts. It leverages the Selenium library for browser automation, uses webdriver-manager for ChromeDriver management, and supports concurrent execution for efficiency. Results are compiled into an HTML report and automatically opened in Firefox.

# Features

    Automated XSS Testing: Automatically injects payloads into specified URL parameters and checks for JavaScript alerts.
    Headless Browser Execution: Uses a headless Chrome browser for testing, which allows for running tests without a visible UI.
    Concurrent Execution: Tests are performed in parallel using Python’s concurrent.futures to speed up the process.
    Custom Payloads: Supports custom payloads loaded from a file.
    HTML Report Generation: Compiles the results into an HTML report with a styled table that lists payloads that triggered alerts.
    Automatic Report Opening: The generated report is automatically opened in Firefox for quick review.
