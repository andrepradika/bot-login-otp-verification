from __future__ import print_function
from utils.getGmailServcies import get_gmail_service
from utils.getVerificationCode import get_verification_code
from utils.utils import click_with_retry
import time
import random
from playwright.sync_api import sync_playwright

def random_delay(min_t=5, max_t=10):
    time.sleep(random.uniform(min_t, max_t))

def random_delay2(min_t=10, max_t=20):
    time.sleep(random.uniform(min_t, max_t))

def login(targetID, targetPass, max_login_retries=3):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
        
        print("Opening Target login page...")
        page.goto("https://target/auth/login/")
        random_delay()
        
        print("Focusing on username field...")
        page.locator("input[name='username']").click()
        for char in targetID:
            page.type("input[name='username']", char, delay=random.randint(80, 150))  
        random_delay()
        
        print("Focusing on password field...")
        page.locator("input[name='password']").click()
        for char in targetPass:
            page.type("input[name='password']", char, delay=random.randint(90, 180))  
        random_delay()

        login_attempts = 0
        while login_attempts < max_login_retries:
            print(f"Attempting login ({login_attempts + 1})...")
            page.locator("button[type='submit']").hover()
            random_delay()
            page.keyboard.press("Enter")
            random_delay2()
            
            print("Checking for login status...")
            random_delay()
            if "extra-verification" in page.url:
                print("Login successful, proceeding to OTP verification.")
                break
            
            error_element = page.locator("text='Terjadi kesalahan, silahkan coba lagi.'")
            if error_element.count() > 0:
                print(f"Login failed. Retrying ({login_attempts + 1}/{max_login_retries})...")
                login_attempts += 1
                random_delay()
            else:
                break  

        if login_attempts == max_login_retries:
            print("Too many failed login attempts. Exiting...")
            browser.close()
            return

        print("Waiting for OTP page...")
        try:
            page.wait_for_selector("input.otp-key", timeout=15000)
        except:
            print("Failed to detect OTP input fields. Exiting...")
            browser.close()
            return
        
        print("Fetching OTP...")
        service = get_gmail_service()
        verification_code = get_verification_code(service)
        print(f'Your OTP: {verification_code}')

        otp_inputs = page.locator("input.otp-key")
        for i, digit in enumerate(verification_code):
            otp_inputs.nth(i).click()
            random_delay(0.2, 0.8)
            otp_inputs.nth(i).type(digit, delay=random.randint(100, 200))
            random_delay()

        print("Submitting OTP...")
        page.locator("button[type='submit']").hover()
        random_delay()
        page.keyboard.press("Enter")
        
        print("Verifying final login status...")
        page.wait_for_load_state("networkidle")
        if "dashboard" in page.url:
            print("Login successful. Accessing dashboard.")
        else:
            print("Login might have failed. Check manually.")
        
        random_delay(10, 20)  
        browser.close()



def main():
    login("", "")
    
if __name__ == '__main__':
    main()
