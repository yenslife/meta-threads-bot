import getpass

from meta_threads_bot.api.login import login_to_threads
from meta_threads_bot.api.post import post_to_threads


def main(caption: str = "感謝 AI 讚嘆 AI"):
    # 輸入使用者名稱和密碼
    username = input("\n請輸入 Threads/Instagram 使用者名稱: ")
    password = getpass.getpass("\n請輸入密碼: ")

    print(f"\n正在嘗試登入 {username} 帳號...")
    cookies = login_to_threads(username=username, password=password)

    if cookies and all(k in cookies for k in ["csrftoken", "sessionid", "ds_user_id"]):
        print("\n成功取得所有必要的 cookies!")
        print(f"csrftoken: {cookies['csrftoken']}")
        print(f"sessionid: {cookies['sessionid']}")
        print(f"ds_user_id: {cookies['ds_user_id']}")

        # 測試發布貼文
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
        print(f"status of response: {response.json()['status']}")
    else:
        print("\n無法取得必要的 cookies，請檢查登入過程")


if __name__ == "__main__":
    # uv run src/meta_threads_bot/api/example.py
    main()
