import time
import getpass

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def post_to_threads(
    caption="Hello World",
    upload_id=None,
    csrf_token=None,
    session_id=None,
    ds_user_id=None,
):
    """
    發布文字貼文到 Threads

    參數:
        caption (str): 貼文內容
        upload_id (str, optional): 上傳 ID，若不指定則使用當前時間戳記

    回傳:
        requests.Response: API 回應物件
    """
    URL = "https://www.threads.net/api/v1/media/configure_text_only_post/"
    # 若未提供 upload_id，則使用當前時間戳記（毫秒）
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))

    # 建立必要的請求資料
    data = {
        "caption": caption,
        "upload_id": upload_id,
        "publish_mode": "text_post",
        "text_post_app_info": f'{{"entry_point":"floating_action_button","text_with_entities":{{"entities":[],"text":"{caption}"}}}}',
    }

    # 建立必要的標頭
    headers = {
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "x-csrftoken": csrf_token,
        "x-ig-app-id": "238260118697367",  # 這是 Threads 官方網頁版 (threads.net) 的 App ID。
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "origin": "https://www.threads.net",
        "referer": "https://www.threads.net/",
    }

    # 建立必要的 cookies
    cookies = {
        "csrftoken": csrf_token,
        "ds_user_id": ds_user_id,
        "sessionid": session_id,
    }

    # 發送 POST 請求
    response = requests.post(URL, headers=headers, cookies=cookies, data=data)

    return response


def login_threads_selenium(username: str, password: str) -> dict[str, str]:
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


def main():
    # 輸入使用者名稱和密碼
    username = input("\n請輸入 Threads/Instagram 使用者名稱: ")
    password = getpass.getpass("\n請輸入密碼: ")

    print(f"\n正在嘗試登入 {username} 帳號...")
    cookies = login_threads_selenium(username=username, password=password)

    if cookies and all(k in cookies for k in ["csrftoken", "sessionid", "ds_user_id"]):
        print("\n成功取得所有必要的 cookies!")
        print(f"csrftoken: {cookies['csrftoken']}")
        print(f"sessionid: {cookies['sessionid']}")
        print(f"ds_user_id: {cookies['ds_user_id']}")

        # 測試發布貼文
        caption = "感謝 AI 讚嘆 AI"
        response = post_to_threads(
            caption=caption,
            csrf_token=cookies["csrftoken"],
            session_id=cookies["sessionid"],
            ds_user_id=cookies["ds_user_id"],
        )

        # 輸出回應狀態碼和內容
        print("\n發布貼文結果:")
        print(f"狀態碼: {response.status_code}")
        print(f"回應內容: {response.text}")
    else:
        print("\n無法取得必要的 cookies，請檢查登入過程")


if __name__ == "__main__":
    # uv run src/meta_threads_bot/threads_api.py
    main()
