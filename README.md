# xssattack

This Python tool is designed to test web applications for Cross-Site Scripting (XSS) vulnerabilities by injecting payloads into specified URL parameters and directly into the URL path. It detects JavaScript alerts to confirm the presence of vulnerabilities. Leveraging the Selenium library for browser automation, it utilizes webdriver-manager for seamless ChromeDriver management and supports concurrent execution for improved efficiency. Results are compiled into an HTML report, which is automatically opened in Firefox on Linux.

This is how it look in the Terminal.

![image](https://github.com/user-attachments/assets/16c5d794-d81c-4203-8bdf-64641d5d2a79)

Note: If you have a custom payload, you can use it here.

# Features

Automated XSS Testing: Automatically injects payloads into specified URL parameters and checks for JavaScript alerts.
Headless Browser Execution: Uses a headless Chrome browser for testing, which allows for running tests without a visible UI.
Concurrent Execution: Tests are performed in parallel using Python’s concurrent.futures to speed up the process.
Custom Payloads: Supports custom payloads loaded from a file.
HTML Report Generation: Compiles the results into an HTML report with a styled table that lists payloads that triggered alerts.
Automatic Report Opening: The generated report is automatically opened in Firefox(linux) or google chrome(windows)for quick review.

# Reqiurements

    pip3 install -r requirements.txt

# Usage

The tool is executed from the command line with several arguments:

 Parameter-Based XSS Testing:
 
    python3 xss-param.py "http://domain.com/index.php?task=" -p "task" -f large-xss.txt -n 10 -o xsstrigers.txt

Arguments:
    
        
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
    
    usage: xss-param.py [-h] -f FILE -p PARAM [-n NUM_PAYLOADS] [-o OUTPUT] url
    
    Detect and handle JavaScript alerts on a webpage.
    
    positional arguments:
      url                   The URL of the target webpage.
    
    options:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  The file containing payloads to test.
      -p PARAM, --param PARAM
                            The name of the URL parameter to insert payloads into.
      -n NUM_PAYLOADS, --num_payloads NUM_PAYLOADS
                            Number of payloads to send from the list.
      -o OUTPUT, --output OUTPUT
                            File to save the output of triggered payloads.

💬 **Integration with Notify** – I’ve added a new feature using the awesome [Notify](https://docs.projectdiscovery.io/tools/notify/overview) tool from Project Discovery! You can now easily send your output to your favorite platforms:

- Slack
- Discord
- Telegram
- Pushover
- Email
- Microsoft Teams
- Google Chat

```bash
python3 xss-param.py "http://domain.com/index.php?task=" -p "task" -f large-xss.txt -n 10 -o xsstrigers.txt; notify -data xsstrigers.txt -bulk
```

# Dependencies

    selenium==4.9.1
    webdriver-manager==4.0.2
    colorama
    rich

Ensure you have these dependencies installed and configured for the tool to function correctly. The webdriver-manager library automatically handles ChromeDriver downloads and updates, so no manual setup is required.
Note

The script assumes that Firefox(linux) is installed at a default location on the system. Adjust the path to the Firefox executable if necessary for different environments.

I wanted to let you know that I'll be regularly updating the wordlist with new payloads I've discovered from various platforms, Please check back every Sunday for the latest updates!
