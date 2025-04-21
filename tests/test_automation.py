from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.image_checker import check_image_validity, ai_detect_issues
import time
import os
import webbrowser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")

print(f"Using OpenAI API Key: {openai_api_key}")

# Global log file path
log_file_path = "test_report.html"

# Clean start: remove previous report and create a new one
def initialize_report():
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    with open(log_file_path, "w") as file:
        file.write(
            "<html><head><title>Test Report</title></head>"
            "<body><h1>Test Automation Report</h1>"
            "<table border='1'><tr><th>Step</th><th>Status</th></tr></table>"
            "<br><h2>AI Issues</h2>"
            "<table border='1'><tr><th>Issue</th><th>Details</th></tr></table><br>"
            "</body></html>"
        )

# Helper function to log results into HTML
def log_to_html(log_message, log_type="info"):
    # Read the current contents of the file
    with open(log_file_path, "r") as file:
        content = file.read()

    # Append the appropriate log based on the type
    if log_type == "info":
        content = content.replace(
            "</table><br><h2>AI Issues</h2>",
            f"<tr><td>{log_message}</td><td>Completed Successfully</td></tr></table><br><h2>AI Issues</h2>"
        )
    elif log_type == "error":
        content = content.replace(
            "</table><br><h2>AI Issues</h2>",
            f"<tr><td>{log_message}</td><td>Error Occurred</td></tr></table><br><h2>AI Issues</h2>"
        )
    elif log_type == "ai":
        content = content.replace(
            "</table><br><h2>AI Issues</h2>",
            f"<tr><td>{log_message}</td><td>Details</td></tr></table><br><h2>AI Issues</h2>"
        )

    # Write the updated content back to the file
    with open(log_file_path, "w") as file:
        file.write(content)

# Helper function to check if an image is valid (not broken)
def check_image_validity(image_url):
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.verify()  # Checks if the image is corrupted or broken

            # Generate a hash value for duplicate detection
            hash_value = imagehash.phash(img)
            return hash_value  # Return hash to compare for duplicates later
        else:
            return None  # Invalid image (not found)
    except Exception as e:
        return None  # In case of any error, treat it as invalid

# Function to detect duplicates based on image hashes
def detect_duplicates(image_hashes):
    seen_hashes = set()
    duplicates = []
    for hash_value in image_hashes:
        if hash_value in seen_hashes:
            duplicates.append(hash_value)  # Collect duplicate hashes
        seen_hashes.add(hash_value)
    return duplicates

# If you need to detect issues like broken images or duplicates
def ai_detect_issues(image_urls):
    image_hashes = [check_image_validity(url) for url in image_urls]
    
    # Detect duplicates in the image hashes
    duplicates = detect_duplicates(image_hashes)
    
    # Identify broken images
    broken_images = [url for url, hash_value in zip(image_urls, image_hashes) if hash_value is None]
    
    # Prepare a report of broken images and duplicates
    report = f"Broken Images: {broken_images}\nDuplicate Image Hashes: {duplicates}"
    return report


def test_full_flow():
    initialize_report()  # Reset report at the start

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        log_to_html("Started Test: OpenHRM Full Flow", "info")

        # Step 1: Open the website
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        log_to_html("Opened Website: https://opensource-demo.orangehrmlive.com", "info")

        # Step 2: Perform Login
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "username"))
        )
        username_field.send_keys("Admin")
        log_to_html("Entered Username", "info")

        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "password"))
        )
        password_field.send_keys("admin123")
        log_to_html("Entered Password", "info")

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        submit_button.click()
        log_to_html("Clicked Submit Button", "info")

        # Validate login success
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
        )
        assert "Dashboard" in driver.page_source, "Login failed!"
        log_to_html("Login Successful: Dashboard visible", "info")

        # Navigation: PIM
        pim_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))
        )
        pim_link.click()
        WebDriverWait(driver, 10).until(EC.url_contains("pim"))
        assert "pim" in driver.current_url, "Navigation to PIM failed."
        log_to_html("Navigation to PIM Successful", "info")

        # Navigation: Leave
        leave_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Leave']"))
        )
        leave_link.click()
        WebDriverWait(driver, 10).until(EC.url_contains("leave"))
        assert "leave" in driver.current_url, "Navigation to Leave page failed."
        log_to_html("Navigation to Leave Successful", "info")

        # Image Check
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
        images = driver.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]

        # AI-powered image validation (local validation and duplicates detection)
        ai_report = ai_detect_issues(image_urls)
        log_to_html("\n--- AI Image Analysis Report ---", "ai")
        log_to_html(ai_report, "ai")

        # Ensure no duplicates in the report (even if the list is empty)
        if "Duplicate Image Hashes: []" in ai_report:
            log_to_html("No Duplicate Image Hashes detected", "info")
        else:
            raise AssertionError("There are duplicate images!")

        # If broken images are detected but we want to tolerate a certain threshold, e.g., max 2 broken images:
        broken_images = [url for url, hash_value in zip(image_urls, ai_report.split("\n")) if "broken" in hash_value]
        
        if len(broken_images) > 2:
            raise AssertionError(f"Too many broken images detected: {len(broken_images)}")
        
        log_to_html("Image Validation Successful", "info")

    except Exception as e:
        os.makedirs("reports", exist_ok=True)
        driver.save_screenshot("reports/error_screenshot.png")
        log_to_html(f"Error Occurred: {e}", "error")
        print(f"Error occurred: {e}")
        raise e

    finally:
        driver.quit()
        webbrowser.open('file://' + os.path.realpath(log_file_path))

# Run the test
test_full_flow()
