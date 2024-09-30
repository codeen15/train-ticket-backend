# Train Ticket App

This README will guide you through the setup process, from installing Python to running the server.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python** (version 3.8 or higher)
- **pip** (Python package installer)

## Step-by-Step Installation Guide

### 1. Install Python

To install Python, follow the instructions for your operating system:

- **Windows**:
  - Download the installer from [python.org](https://www.python.org/downloads/).
  - Run the installer and ensure you check the box that says "Add Python to PATH".

- **macOS**:
  - You can install Python using Homebrew. Open your terminal and run:
    ```bash
    brew install python
    ```

- **Linux**:
  - Use your package manager. For Ubuntu, run:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    ```

### 2. Create a Virtual Environment

Once Python is installed, you should create a virtual environment to manage your dependencies:

1. Open your terminal or command prompt.
2. Navigate to your project directory:
   ```bash
   cd /path/to/your/project
   ```
3. Create a virtual environment named venv:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:

    Windows:
    ```bash
    venv\Scripts\activate
    ```

    macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

### 3. Install Dependencies

With your virtual environment activated, install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
    
### 4. Set Up Environment Variables

Create a .env file in your project root directory to store environment variables. Here are some common variables you might need:
    ```
    EMAIL_HOST="smtp.gmail.com'"
    EMAIL_PORT="587"
    EMAIL_HOST_USER="youremail@gmail.com"
    EMAIL_HOST_PASSWORD="YourPassword Or App Password"
    ```

### 5. Run Database Migrations
    ```
    python manage.py migrate
    ```
    
### 6. Start the Development Server
    ```
    python manage.py runserver
    ```
