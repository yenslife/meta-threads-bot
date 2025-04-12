import time
import requests

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
