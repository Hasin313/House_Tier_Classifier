import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Set up and return a configured Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-webgl")
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.111 Safari/537.36")


    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def download_image(img_url, output_folder, index, url_index):
    """Download a single image and save it to the output folder"""
    try:
        print(f"Downloading image {index + 1} from {img_url}")
        response = requests.get(img_url, timeout=20, stream=True)
        response.raise_for_status()
        
        # Extract file extension
        content_type = response.headers.get('content-type', '').lower()
        ext = 'jpg' if 'jpeg' in content_type or 'jpg' in content_type else 'png' if 'png' in content_type else 'jpg'
        
        # Create folder for each URL
        url_folder = os.path.join(output_folder, f"property_{url_index}")
        os.makedirs(url_folder, exist_ok=True)
        
        filename = f'image_{index + 1}.{ext}'
        filepath = os.path.join(url_folder, filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Successfully downloaded {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {img_url}: {str(e)}")
        return False

# def process_property_page(driver, url, url_index):
#     """Process a single property page"""
#     print(f"\nProcessing URL {url_index}: {url}")
    
#     try:
#         # Clear cookies and cache
#         driver.delete_all_cookies()
        
#         # Load the page with retries
#         for attempt in range(3):
#             try:
#                 driver.get(url)
#                 WebDriverWait(driver, 30).until(
#                     lambda d: d.execute_script('return document.readyState') == 'complete'
#                 )
#                 break
#             except Exception as e:
#                 if attempt == 2:
#                     raise
#                 print(f"Retry {attempt + 1}/3 for URL {url_index}")
#                 time.sleep(5)
        
#         # Try to click photos button with multiple selectors
#         button_selectors = [
#             '//button[contains(., "photos")]',
#             '//button[contains(., "Photos")]',
#             '//button[contains(., "PHOTOS")]',
#             '//*[@id="photoPreviewButton"]'
#         ]
        
#         for selector in button_selectors:
#             try:
#                 photos_button = WebDriverWait(driver, 15).until(
#                     EC.element_to_be_clickable((By.XPATH, selector))
#                 )
#                 print("Clicking photos button...")
#                 driver.execute_script("arguments[0].click();", photos_button)
#                 time.sleep(3)
#                 break
#             except:
#                 continue
        
#         # Wait for and scroll through the photo gallery
#         WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bp-PhotoArea'))
#         )
        
#         # Scroll to load all images
#         print("Scrolling to load all images...")
#         photo_area = driver.find_element(By.CSS_SELECTOR, 'div.bp-PhotoArea')
#         last_height = driver.execute_script("return arguments[0].scrollHeight", photo_area)
#         scroll_attempts = 0
        
#         while scroll_attempts < 5:
#             driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", photo_area)
#             time.sleep(2)
#             new_height = driver.execute_script("return arguments[0].scrollHeight", photo_area)
#             if new_height == last_height:
#                 break
#             last_height = new_height
#             scroll_attempts += 1
        
#         # Find all property images (FIXED SYNTAX ERROR HERE)
#         image_elements = WebDriverWait(driver, 20).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.bp-PhotoArea img.img-card'))
#         )
#         print(f"Found {len(image_elements)} property images")
        
#         if not image_elements:
#             print("No property images found")
#             return
        
#         # Download all images
#         for i, img in enumerate(image_elements, 1):
#             img_url = img.get_attribute('src') or img.get_attribute('data-src')
#             if img_url:
#                 clean_url = img_url.split('?')[0]
#                 if not download_image(clean_url, 'property_images', i, url_index):
#                     print(f"Retrying image {i}...")
#                     time.sleep(3)
#                     download_image(clean_url, 'property_images', i, url_index)
#             else:
#                 print(f"Image {i} has no src attribute")
                
#     except Exception as e:
#         print(f"Error processing URL {url_index}: {str(e)}")
#         with open(f'error_property_{url_index}.html', 'w', encoding='utf-8') as f:
#             f.write(driver.page_source)
#         print(f"Saved error page to error_property_{url_index}.html")


def process_property_page(driver, url, url_index, retries=3):
    """Process a single property page with retry logic"""
    print(f"\nProcessing URL {url_index}: {url}")
    
    try:
        # Clear cookies and cache
        driver.delete_all_cookies()

        # Load the page with retries
        for attempt in range(retries):
            try:
                driver.get(url)
                WebDriverWait(driver, 30).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )
                break  # Break out of the loop if successful
            except Exception as e:
                if attempt == retries - 1:
                    raise  # Raise the error if it's the final retry
                print(f"Retry {attempt + 1}/{retries} for URL {url_index}")
                time.sleep(5)
        
        # Try to click photos button with multiple selectors
        button_selectors = [
            '//button[contains(., "photos")]',
            '//button[contains(., "Photos")]',
            '//button[contains(., "PHOTOS")]',
            '//*[@id="photoPreviewButton"]'
        ]
        
        for selector in button_selectors:
            try:
                photos_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print("Clicking photos button...")
                driver.execute_script("arguments[0].click();", photos_button)
                time.sleep(3)
                break
            except:
                continue
        
        # Wait for and scroll through the photo gallery
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bp-PhotoArea'))
        )
        
        # Scroll to load all images
        print("Scrolling to load all images...")
        photo_area = driver.find_element(By.CSS_SELECTOR, 'div.bp-PhotoArea')
        last_height = driver.execute_script("return arguments[0].scrollHeight", photo_area)
        scroll_attempts = 0
        
        while scroll_attempts < 5:
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", photo_area)
            time.sleep(2)
            new_height = driver.execute_script("return arguments[0].scrollHeight", photo_area)
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1
        
        # Find all property images (FIXED SYNTAX ERROR HERE)
        image_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.bp-PhotoArea img.img-card'))
        )
        print(f"Found {len(image_elements)} property images")
        
        if not image_elements:
            print("No property images found")
            return
        
        # Download all images
        for i, img in enumerate(image_elements, 1):
            img_url = img.get_attribute('src') or img.get_attribute('data-src')
            if img_url:
                clean_url = img_url.split('?')[0]
                if not download_image(clean_url, 'property_images', i, url_index):
                    print(f"Retrying image {i}...")
                    time.sleep(3)
                    download_image(clean_url, 'property_images', i, url_index)
            else:
                print(f"Image {i} has no src attribute")
                
    except Exception as e:
        print(f"Error processing URL {url_index}: {str(e)}")
        with open(f'error_property_{url_index}.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"Saved error page to error_property_{url_index}.html")

        # Retry the URL if there was an error
        if retries > 0:
            print(f"Retrying URL {url_index} after failure...")
            time.sleep(5)
            process_property_page(driver, url, url_index, retries - 1)



def main():
    # Read URLs from Excel
    excel_path = r'C:\Users\hasin\OneDrive\Desktop\Se_project\filtered_df_cleaned.csv'
    df = pd.read_csv(excel_path)
    urls = df['url'].dropna().tolist()
    
    # Process in batches with fresh browser sessions
    batch_size = 5
    for batch_start in range(0, len(urls), batch_size):
        batch_urls = urls[batch_start:batch_start + batch_size]
        print(f"\n=== Processing batch {batch_start//batch_size + 1} ===")
        
        driver = setup_driver()
        try:
            for i, url in enumerate(batch_urls, 1):
                url_index = batch_start + i
                process_property_page(driver, url, url_index)
                time.sleep(4)
        finally:
            driver.quit()
            print("Browser session refreshed")
            time.sleep(3)
    
    print("All properties processed successfully")

if __name__ == "__main__":
    main()