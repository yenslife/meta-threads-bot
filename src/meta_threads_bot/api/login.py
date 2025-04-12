from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def login_to_threads(username: str, password: str) -> dict[str, str]:
    """
    使用 Selenium 模擬登入 Threads，並取得必要的 cookies

    參數:
        username (str): Threads/Instagram 使用者名稱
        password (str): Threads/Instagram 密碼

    回傳:
        dict: 包含 csrftoken、sessionid 和 ds_user_id 的 cookies 字典
    """
    options = webdriver.ChromeOptions()
    # 無頭模式設定
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")  # 設定視窗大小，避免元素不可見

    # 避免被偵測為自動化工具
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    # 修改 navigator.webdriver 標記
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    try:
        # 前往登入頁面
        driver.get("https://www.threads.net/login")
        print("🌐 正在載入登入頁面...")
        time.sleep(5)  # 等待頁面完全載入

        # 使用 CSS 選擇器定位輸入框
        user_input = driver.find_element(
            By.CSS_SELECTOR, "input[autocomplete='username']"
        )
        print("✅ 找到使用者名稱輸入框")

        # 輸入使用者名稱
        user_input.clear()
        user_input.send_keys(username)
        time.sleep(1)

        # 定位密碼輸入框
        pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        print("✅ 找到密碼輸入框")

        # 輸入密碼
        pass_input.clear()
        pass_input.send_keys(password)
        time.sleep(1)

        # 點擊登入按鈕 (根據提供的 HTML 結構)
        # 嘗試多種可能的選擇器
        try:
            # 嘗試找到具有「登入」文字的按鈕
            login_button = driver.find_element(
                By.XPATH,
                "//div[contains(text(), '登入')]/ancestor::div[@role='button']",
            )
            print("✅ 找到登入按鈕 (通過文字內容)")
        except Exception:
            try:
                # 嘗試找到表單提交按鈕
                login_button = driver.find_element(
                    By.CSS_SELECTOR, "button[type='submit']"
                )
                print("✅ 找到登入按鈕 (通過 type='submit')")
            except Exception:
                # 最後嘗試通過角色找到按鈕
                login_button = driver.find_element(
                    By.CSS_SELECTOR, "div[role='button']"
                )
                print("✅ 找到登入按鈕 (通過 role='button')")

        # 點擊登入按鈕
        login_button.click()
        print("👆 已點擊登入按鈕")

        # 等待登入成功並跳轉
        print("⏳ 等待登入處理中...")
        time.sleep(10)

        # 檢查是否登入成功 (可能會跳轉到主頁或其他頁面)
        current_url = driver.current_url
        print(f"🔗 當前網址: {current_url}")

        if "threads.net" in current_url and "login" not in current_url:
            print("✅ 登入成功!")

            # 取得 Cookies
            cookies = driver.get_cookies()
            cookie_dict = {cookie["name"]: cookie["value"] for cookie in cookies}

            # 提取需要的 cookies
            result = {}
            if "csrftoken" in cookie_dict:
                result["csrftoken"] = cookie_dict["csrftoken"]
            if "sessionid" in cookie_dict:
                result["sessionid"] = cookie_dict["sessionid"]
            if "ds_user_id" in cookie_dict:
                result["ds_user_id"] = cookie_dict["ds_user_id"]

            print(f"🍪 已取得必要的 cookies: {', '.join(result.keys())}")
            return result
        else:
            print("❌ 登入失敗，請檢查使用者名稱和密碼")
            return None

    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        return None
    finally:
        # 關閉瀏覽器
        driver.quit()
        print("🔒 瀏覽器已關閉")
