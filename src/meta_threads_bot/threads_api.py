import requests
import time

# Threads API 網址
URL = "https://www.threads.net/api/v1/media/configure_text_only_post/"

def post_to_threads(caption="Hello World", upload_id=None, csrf_token=None, session_id=None, ds_user_id=None):
    """
    發布文字貼文到 Threads

    參數:
        caption (str): 貼文內容
        upload_id (str, optional): 上傳 ID，若不指定則使用當前時間戳記

    回傳:
        requests.Response: API 回應物件

    目前發現只要 header 少任何一個東西，就會需要重新登入
    """
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
        "x-ig-app-id": "238260118697367", # 這是 Threads 官方網頁版 (threads.net) 的 App ID。
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


def login_and_get_cookies():
    # TODO: 實現登入功能
    pass


def main():
    # 請替換以下資訊為您的實際資訊
    # 這三個最重要，登入後可以找到，在 cookies 中
    csrf_token = ""
    session_id = ""
    ds_user_id = ""

    # 發布貼文
    caption = "這是一則測試貼文！999"
    response = post_to_threads(caption=caption, csrf_token=csrf_token, session_id=session_id, ds_user_id=ds_user_id)
    print(response)

    # 輸出回應狀態碼和內容
    print(f"狀態碼: {response.status_code}")
    print(f"回應內容: {response.text}")


if __name__ == "__main__":
    # uv run src/meta_threads_bot/threads_api.py
    main()
