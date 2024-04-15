# Code Efficiency Enhancer AI

The Code Efficiency Enhancer AI is an innovative Flask-based application that connects with Cisco Webex Teams to introduce a new paradigm in smart and sustainable coding. Utilizing the prowess of AI, this chatbot provides developers with an analysis of their code's power consumption and CPU utilization, coupled with actionable recommendations to refine code for optimal performance and environmental friendliness.


Containerized for convenience and portability with Docker, the Code Efficiency Enhancer AI is a testament to eco-conscious development practices and Cisco's commitment to advanced networking capabilities.


- Technology stack: Python, Flask, Docker, OpenAI API, Cisco Webex Teams API
- Status: Beta - Eager to evolve with community input and collaborative enhancements.

## Use Case

Code Efficiency Enhancer AI is engineered for forward-thinking developers dedicated to crafting efficient, high-performance software while minimizing environmental impact. By analyzing code snippets and offering insights on energy consumption and CPU cycles, the chatbot empowers developers to:


- Elevate code quality with smart optimization strategies.
- Reduce the ecological footprint of software by optimizing resource usage.
- Leverage Cisco's advanced networking capabilities to support sustainable coding practices.

The AI doesn't merely analyze—it inspires developers to push beyond the conventional, fostering a culture of eco-friendly and efficient programming.

## Installation

To deploy the Code Efficiency Enhancer AI using Docker, follow these steps:

Clone the repository:

```
git clone https://github.com/shiiks/code-efficiency-enhancer-ai.git
```

Navigate to your project folder:

```
cd code-efficiency-enhancer-ai
```

Create the .env file in this format:

```
CLIENT_ID=<CLIENT_ID>
CLIENT_SECRET=<CLIENT_SECRET>
APP_KEY=<CLIENT_SECRET>
OAUTH_URL=<OAUTH_URL>
AZURE_ENDPOINT=<AZURE_ENDPOINT>
API_VERSION=<API_VERSION>
GPT_MODEL=<GPT_MODEL>
BOT_NAME=<BOT_NAME>
BOT_FULL_NAME=<BOT_FULL_NAME>
CHATBOT_TOKEN=<CHATBOT_TOKEN>
CHATBOT_DEBUG=True
CHATBOT=https://127.0.0.1:8080
WEBEX_MESSAGE_URL=<WEBEX_MESSAGE_URL>
WEBEX_BOT_ACCESS_TOKEN=<WEBEX_BOT_ACCESS_TOKEN>
WEBEX_BOT_EMAIL=<WEBEX_BOT_EMAIL>
FLASK_APP=chatbot.py
LOG_PATH=.
LOG_FILE=code-efficiency-enhancer-ai.log
LOG_LEVEL=DEBUG
PROMPT_FILE=prompt.txt
```

Build the Docker image:

```
docker build -t code-efficiency-enhancer-ai .
```

Run the Docker container:

```
docker run --env-file .env -it -p 8080:8080 code-efficiency-enhancer-ai
```

The application will be accessible at http://localhost:8080 or the corresponding network IP and port if deployed on a server or VM.

## Configuration

### Setting up ngrok for Local Development

When developing and testing the Code Efficiency Enhancer AI locally, you will need to expose your local server to the internet to receive webhook notifications from Webex Teams. ngrok can create a secure tunnel to your localhost, allowing you to share your local server on the internet.

### Installing ngrok

If you haven't already installed ngrok, download it from https://ngrok.com/download and follow the installation instructions for your platform.

### Starting ngrok

After installation, start an ngrok tunnel to your application's port (e.g., 8080) with the following command:

```
ngrok http 8080
```

ngrok will provide a public URL that forwards to your local development server.

### Configuring Webex Teams Webhook

Copy the ngrok forwarding URL (e.g., https://<random-id>.ngrok.io) and use it to configure the webhook in Webex Teams. The Webex Teams platform will send notifications to this URL, which will be routed to your local server.


Make sure your Flask application can handle the Webex Teams webhook payloads. For webhook setup on Webex Teams, visit [Webex for Developers](https://developer.webex.com/docs/api/guides/webhooks).

### Keep ngrok Running

Keep the ngrok session active while developing to maintain the webhook functionality. If ngrok stops, the URL will not forward to your server, and you will need to provide a new URL to Webex Teams.

## Usage

Once the Docker container and ngrok are operational, developers can interact with the Code Efficiency Enhancer AI within Webex Teams. The chatbot will analyze code snippets and provide suggestions for enhancing efficiency and sustainability.


To halt the Docker container:

```
docker stop code_efficiency_ai
```

To discard the Docker container:

```
docker rm code_efficiency_ai
```

Refer to the USAGE.md file for comprehensive instructions, examples, and command references.

## Related Sandbox

Experiment with the Code Efficiency Enhancer AI in a controlled environment using the Webex Teams sandbox provided by DevNet:
[Webex Teams Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/38dd7fc0-3727-4a08-8ad4-eac5c5a3a1f6)

## Getting help

Should you encounter difficulties or have inquiries regarding the application, please raise an issue on the GitHub repository or consult the SUPPORT.md file for further guidance.

## Getting involved

Contributors to the Code Efficiency Enhancer AI project are highly appreciated. If you wish to contribute to the project's evolution or propose new features, please see the CONTRIBUTING.md file for contribution guidelines.

## Credits and references

This project is a beacon of innovation, merging the cutting-edge natural language processing of OpenAI with the robustness of the Flask web framework and Cisco's networking prowess to guide software development towards a greener future.

## License
This script is licensed under the BSD 3-Clause License. See the LICENSE file for more information.