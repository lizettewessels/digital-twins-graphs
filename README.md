# digital-twins-graphs

Using Python to extract information from BibTeX files and produce graphs on the topic of Digital Twins.

## Requirements
This project uses Python 3.11 and was tested on Ubuntu and Linux Mint.

## Setup Instructions for Linux Users
Follow these steps to set up the project on your Linux system:

1. **Create a Virtual Environment:**
   Use `virtualenv` to create a virtual environment named `ve`.
   ```bash
   virtualenv ve -p /usr/bin/python3.11
   ```

2. **Upgrade pip:**
   Upgrade pip in the virtual environment to version 24.0.
   ```bash
   ./ve/bin/pip install --upgrade pip==24.0
   ```

3. **Install Requirements:**
   Install the required Python packages using the `requirements.txt` file.
   ```bash
   ./ve/bin/pip install -r requirements.txt
   ```

4. **Process Data:**
   Run `process_data.py` to convert raw BibTeX data into JSON format. Make sure to use the Python executable from your virtual environment.
   ```bash
   ./ve/bin/python process_data.py
   ```

5. **Create Graphs:**
   Execute `create_graphs.py` to generate the plots. This script will save the graphs in a newly created `graphs` folder.
   ```bash
   ./ve/bin/python create_graphs.py
   ```

Ensure you follow these steps in order to set up and run the scripts properly on your Linux machine.

## Setup Instructions for Windows Users
Follow these steps to set up the project on your Windows system:

### Prerequisites
1. **Install Python:**
   - Visit the official Python website ([python.org](https://www.python.org/downloads/)) and download the latest version of Python 3.11 for Windows.
   - Run the downloaded installer. Ensure you check the box that says **Add Python 3.11 to PATH** before clicking **Install Now**.

2. **Install Git:**
   - Download Git for Windows from [git-scm.com](https://git-scm.com/download/win).
   - Run the installer. Accept the default options unless you have specific preferences.

### Setting Up Your Environment
3. **Open PowerShell:**
   - You can open PowerShell by searching for it in the start menu. Right-click on it and select **Run as administrator**.

4. **Create a Projects Directory:**
   - Decide where you want your projects directory to be. For example, you can create it in your Documents.
   - In PowerShell, navigate to your chosen directory:
     ```bash
     cd Documents
     ```
   - Create a new folder for your projects and navigate into it:
     ```bash
     mkdir projects
     cd projects
     ```

5. **Clone the Repository:**
   - Clone the `digital-twins-graphs` repository into the `projects` directory:
     ```bash
     git clone [https://github.com/lizettewessels/digital-twins-graphs.git](https://github.com/lizettewessels/digital-twins-graphs.git)
     cd digital-twins-graphs
     ```
   - When prompted, enter your GitHub username and then your password. Note: If you have two-factor authentication enabled, you might need to generate and use a personal access token as a password.


6. **Create a Virtual Environment:**
   - Install the `virtualenv` package if it is not already installed:
     ```bash
     pip install virtualenv
     ```
   - Create a virtual environment named `ve`:
     ```bash
     virtualenv ve
     ```

7. **Activate the Virtual Environment:**
   - Activate the virtual environment:
     ```bash
     .\ve\Scripts\activate
     ```

8. **Upgrade pip:**
   - It's a good practice to ensure your package manager is up-to-date. Upgrade pip to version 24.0 within the virtual environment:
     ```bash
     pip install --upgrade pip==24.0
     ```

9. **Install Requirements:**
   - Install the required Python packages using the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

### Running the Project
10. **Process Data:**
   - Run the script to convert raw BibTeX data into JSON format:
     ```bash
     python process_data.py
     ```

11. **Create Graphs:**
   - Execute the script to generate the plots. This will save the graphs in a newly created `graphs` folder:
     ```bash
     python create_graphs.py
     ```

Ensure you follow these steps in order to set up and run the scripts properly on your Windows machine.
