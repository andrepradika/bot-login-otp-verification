Here’s an improved **README** with an **explanation of the code** along with the **license** and **author details**.  

---

# 🔐 Automated Login & OTP Verification  

This project automates the **login process** for a website that requires **OTP-based authentication**. It uses **Playwright** 🎭 for browser automation and **Gmail API** 📩 to fetch OTP codes from an email account.

---

## 🚀 Features  

✅ **Automated Login** – Enters username and password like a real user.  
✅ **OTP Handling** – Fetches the verification code from Gmail.  
✅ **Randomized Delays** – Mimics human behavior to bypass detection.  
✅ **Retry Mechanism** – Handles failed login attempts.  
✅ **Playwright Automation** – Uses a headless browser for efficiency.  

---

## 🏷️ Topics  

🔹 **Web Automation** 🌍 – Automate login flows using Playwright.  
🔹 **Email API** 📩 – Fetch OTP codes from Gmail.  
🔹 **Python Scripting** 🐍 – Automate repetitive tasks.  
🔹 **Bot Detection Bypass** 🔄 – Mimic real user behavior with random delays.  
🔹 **Cybersecurity & Testing** 🔑 – Secure login testing and automation.  

---

## 📂 Setup  

### 1️⃣ Install Dependencies  
```bash
pip install playwright google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
playwright install
```

### 2️⃣ Set Up Gmail API  
- Enable Gmail API in **Google Cloud Console**.  
- Download `credentials.json` and place it in the `utils/` folder.  

### 3️⃣ Run the Script  
```bash
python login.py
```

---

## 📝 Code Explanation  

### **1️⃣ Import Dependencies**  
```python
from __future__ import print_function
from utils.getGmailServcies import get_gmail_service
from utils.getVerificationCode import get_verification_code
from utils.utils import click_with_retry
import time
import random
from playwright.sync_api import sync_playwright
```
- `playwright.sync_api` – Automates browser actions.  
- `get_gmail_service` – Connects to Gmail API.  
- `get_verification_code` – Extracts OTP from emails.  
- `time.sleep()` & `random.uniform()` – Adds **human-like delays**.  

---

### **2️⃣ Define Random Delays**  
```python
def random_delay(min_t=5, max_t=10):
    time.sleep(random.uniform(min_t, max_t))
```
- Adds **random wait times** to **avoid bot detection**.  

---

### **3️⃣ Automate Login Process**  
```python
def login(targetID, targetPass, max_login_retries=3):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(user_agent="Mozilla/5.0 ...")
        
        print("Opening login page...")
        page.goto("https://target/auth/login/")
        random_delay()
```
- Opens the **login page** using a **realistic browser**.  
- Uses a **custom user-agent** to **avoid bot detection**.  

---

### **4️⃣ Enter Username & Password**  
```python
        print("Entering username...")
        page.locator("input[name='username']").click()
        for char in targetID:
            page.type("input[name='username']", char, delay=random.randint(80, 150))  
        random_delay()
```
- Simulates **typing speed** to **mimic human behavior**.  

---

### **5️⃣ Login Retry Mechanism**  
```python
        login_attempts = 0
        while login_attempts < max_login_retries:
            print(f"Attempting login ({login_attempts + 1})...")
            page.locator("button[type='submit']").hover()
            random_delay()
            page.keyboard.press("Enter")
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
```
- **Retries login** up to 3 times **if it fails**.  
- **Checks the page URL** to see if **OTP verification is required**.  

---

### **6️⃣ Fetch OTP from Gmail**  
```python
        print("Fetching OTP...")
        service = get_gmail_service()
        verification_code = get_verification_code(service)
        print(f'Your OTP: {verification_code}')
```
- Uses **Gmail API** to retrieve the **OTP code**.  

---

### **7️⃣ Enter OTP & Final Verification**  
```python
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
```
- **Types the OTP digits one by one**.  
- **Submits the OTP** and checks if the **dashboard loads**.  

---

## License

MIT License (or your preferred license)

## Author
andrepradika