# OrangeHRM Selenium Test Automation

This project is a UI Automation Test using Python, Selenium WebDriver, and Pytest for the OrangeHRM Open Source Demo website.

## 💡 Project Overview

This automation script covers:

- Login validation for OrangeHRM.
- Navigation to important modules (`PIM`, `Leave`, `Time`, `Recruitment`, `Performance`, `Directory`, `Claim`, `Buzz` ).
- Image validation using AI-assisted duplicate & broken image detection.
- Automated HTML Report generation.

---

## 🧰 Technologies Used

- **Python 3.x**
- **Selenium WebDriver**: For browser automation.
- **PyTest**: For running tests and managing test cases.
- **OpenAI API**: For AI-powered image analysis.
- **dotenv**: For managing environment variables.
- **Pillow**: For image handling and validation.
- **requests**: For making HTTP requests to retrieve images.
- **imagehash**: For detecting duplicate images using perceptual hashes.

---

## ⚡ How to Run the Tests

1. Clone the repository:
   git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   cd YOUR_REPOSITORY
   (Check the Troubleshooting at the bottom)

3. Set Up the Environment
Install Python & Virtual Environment
Ensure that Python 3.x is installed on your system. You can check this by running:

python --version
Next, create a virtual environment to isolate the dependencies:

python -m venv venv
Activate the virtual environment:

On Windows:

venv\Scripts\activate
On macOS/Linux:

source venv/bin/activate
Install Required Packages
Once the virtual environment is activated, install the necessary dependencies using pip:

pip install -r requirements.txt
This will install all the required Python libraries listed in the requirements.txt file.

3. Set Up OpenAI API Key
In order to use AI-powered image validation, you'll need an OpenAI API key.

Go to OpenAI and sign up or log in to generate your API key.

Create a .env file in the project root directory and add your OpenAI API key as follows:

OPENAI_API_KEY=your-openai-api-key
Make sure to replace your-openai-api-key with your actual OpenAI API key.

⚡ Running the Tests
Once everything is set up, you can run the automated UI tests with the following command:

pytest test_script.py
This will:

Run the Selenium WebDriver tests.

Include the AI image validation.

Generate an HTML report with results and AI insights.

📝 Report Generation
After the test run completes, an HTML report (test_report.html) will be generated. You can open this report in your browser to view:

Test Execution Details: Overview of the test steps and their status.

AI Image Validation Insights: Information on broken and duplicate images, along with AI insights.

❗ Troubleshooting
Missing API Key: If you encounter errors regarding the OpenAI API, ensure the .env file is correctly configured with a valid API key.

Internet Connectivity: The tests require an internet connection to fetch images and communicate with the OpenAI API.

Selenium WebDriver: Ensure you have the correct browser driver installed (e.g., ChromeDriver for Google Chrome) and accessible in your system PATH.

If you encounter "Encountered 7 files that should have been pointers, but weren't:"

1. Ensure Git LFS is Installed
Before cloning the repository, make sure Git LFS is installed on your machine. If it’s not installed, follow these instructions:

Windows: Download the installer from Git LFS.

macOS: You can install it via Homebrew:

brew install git-lfs
Linux: Follow the instructions on the Git LFS GitHub page for your specific distribution.

2. Clone the Repository
Once Git LFS is installed, you can clone the repository as usual. Run the following command in your terminal:

git clone https://github.com/arcorivera/test-automation.git
This will clone the repository, but since the large files are tracked with Git LFS, Git will not download them automatically just yet. Instead, it will create pointers for those files.

3. Pull the Large Files Using Git LFS
After cloning the repository, navigate into the project directory:

cd test-automation
Now, to download the actual content for the large files tracked by Git LFS, run:

git lfs pull
This command tells Git LFS to download the large files and replace the pointers with the actual content.

4. Verify the Files
Once the LFS files have been downloaded, you can verify that the large files are now in place by checking the drivers/chrome-win32/ folder. You should see the actual .dll files and other large files instead of the pointer files.

5. Make Changes or Test the Project
You can now proceed to make any changes or run tests with the project as usual. The large files tracked by Git LFS will behave like normal files in the repository, but they are stored separately by Git LFS to keep the Git history clean.

OR

Download `chromedriver.exe` manually from:
https://chromedriver.chromium.org/downloads
and place it in the `drivers/` folder.
