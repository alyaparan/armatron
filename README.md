# Armatron Exploitation Tool v1.0

## Overview

The Armatron Exploitation Tool (ArmExploit) is a powerful script designed for conducting targeted web exploitation. It facilitates sending HTTP requests with customizable parameters such as payloads, user-agents, headers, and cookies to identify vulnerabilities and potentially exploit them.

## Features

- Flexible Configuration: Customize HTTP requests with various parameters including payloads, user-agents, headers, and cookies.

- Concurrent Exploitation: Execute multiple exploit attempts concurrently to enhance efficiency.
    
- Payload and User-Agent Management: Load payloads and user-agents from external files for easy management and customization.
    
- HTTP Method Support: Supports common HTTP methods including GET, POST, PUT, and DELETE.
    
- HTTP Basic Authentication: Optionally provide HTTP basic authentication credentials for accessing protected resources.
    
- Verbose and Debug Modes: Enable verbose and debug modes for detailed logging and debugging information.
    
- SSL Certificate Verification: Option to enable or disable SSL certificate verification for target URLs.

## Usage
Installation

Clone the repository:

```bash

git clone https://github.com/alyaparan/armatron.git
```

Navigate to the project directory:

```bash

cd armatron
```

Install the required dependencies:

```bash

pip install -r requirements.txt
```

Usage

Run the script using the following command:

```bash

python3 Armatron.py --help

```

Replace [options] with the desired command-line options to customize the exploit parameters.

## Command-line Options

- --url: Specify the target URL (default: http://target-server.com).
- --uri: Specify the target URI (default: /).
- --method: Specify the HTTP method to use (default: POST).
- --param: Specify parameters.
- --value: Specify parameter values.
- --cookie: Specify cookies.
- --payload-file: Specify the file containing payloads (default: payloads.txt).
- --user-agents-file: Specify the file containing user agents (default: user_agents.txt).
- --headers: Specify custom headers as key-value pairs separated by ':'.
- --proxy: Specify the proxy server URL.
- --auth: Specify HTTP basic authentication credentials as username and password.
- --verbose: Enable verbose mode.
- --debug: Enable debug mode.
- --concurrency: Specify the number of concurrent threads (default: 10).
- --no-ssl-verify: Disable SSL certificate verification.
- --interactive: Enable interactive mode.
- --rate-limit: Specify the requests per second rate limit (default: 0, no limit).
- --timeout: Specify the timeout for each request in seconds (default: 10).
- --retries: Specify the number of retries for failed requests (default: 3).
- --output-file: Specify the output file to save the results.

## Disclaimer

The Armatron Exploitation Tool is for educational purposes only. Use it responsibly and legally. The developer assumes no liability for any misuse or damage caused by the tool.

## Contribution

If you have suggestions or improvements, feel free to contribute. Follow the guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the License 2.0 apache github - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

For questions or concerns, you can contact the project creator at Website www.alikparanyan.com or Email mail@alikparanyan.com or personal gmail alikparanyan@gmail.com.
