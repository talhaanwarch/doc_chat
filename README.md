# Scalable Web Application for PDF Chat using ChatGPT

Welcome to our Web Application for PDF Chat powered by OpenAI's ChatGPT! This application allows users to upload PDF documents, utilize ChatGPT for natural language processing, and engage in interactive conversations with their data. Each user's data is kept separate from others, ensuring privacy and security.  

Website: https://gptdemo.talhaanwar.com/  
Dasboard: https://dashboard.talhaanwar.com/  
Server: https://server-monitor.talhaanwar.com/  

This README will guide you through the deployment and usage of the application.  

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Web Application for PDF Chat is designed to provide an interactive and user-friendly experience for users to engage with their uploaded PDF documents. The application integrates OpenAI's GPT-3.5, which is a powerful natural language processing model, to enable seamless conversations and answer retrieval based on user queries. The backend is built using FastAPI, and user authentication is also included to ensure secure access to individual data.

## Features

- Upload PDF documents for processing and analysis.
- Engage in interactive conversations with the uploaded data using OpenAI's GPT-3.5.
- Retrieve answers to specific questions from the uploaded PDFs.
- Secure user authentication and data separation to ensure privacy.
- Dashboard powered by AppSmith for easy navigation and visualization.

## Prerequisites

Before deploying the application, ensure that you have the following components:

1. Docker
2. Docker Compose
3. S3 account
4. OpenAI API

## Installation

1. Clone the repository from GitHub:

```bash
git clone https://github.com/talhaanwarch/doc_chat.git
```

2. Navigate to the project directory:

```bash
cd doc_chat
```

3. Create an `.env` file and set the required environment variables. You can use the `example.env` file as a reference.

```bash
cp example.env .env
```

4. Build and deploy the application using the provided `deploy.sh` script:

```bash
./deploy.sh
```

This script will stop and remove any existing Docker containers, clear dangling volumes, and then deploy the three Docker Compose files for the backend, Milvus vector database, and ToolJet dashboard.

## Usage

Once the application is successfully deployed, you can access the following pages from your web browser:

- **Upload Page:** This page allows users to upload their PDF documents for processing.

- **Query Page:** Engage in interactive conversations with your uploaded PDF data. Ask questions, get answers, and explore the content.

- **Login Page:** Securely log in to access your uploaded data. Each user's data is separated from others.

- **Logout Page:** Log out from your session to ensure data privacy.

- **Registration Page:** New users can register to create an account and start using the application.

## Technologies Used

The Web Application for PDF Chat leverages the following technologies:

- FastAPI: For building the backend and handling user authentication.
- Flask: For the frontend and user interface.
- PostgreSQL: As the database for user-related information.
- Docker: For containerizing the application and its components.
- Docker Compose: For orchestrating the deployment of multiple containers.
- Milvus: As the vector database for efficient data retrieval.
- Appsmith: For creating the interactive dashboard.
- Netdata: For server monitoring 

## Contributing

We welcome contributions to enhance the features and usability of our Web Application for PDF Chat. If you find any bugs or have suggestions for improvements, please feel free to open issues or submit pull requests.

## License

The Web Application for PDF Chat is open-source and available under the CC-BY-NC. You are free to use, modify, and distribute the code as per the terms of the license.

---

Thank you for using our Web Application for PDF Chat! If you have any questions or need further assistance, please don't hesitate to contact us or raise an issue on GitHub. Happy chatting with your data!
