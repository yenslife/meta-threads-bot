# 這是一個可以自動瀏覽 threads 的 API
# 使用 selenium 模擬瀏覽器操作
from selenium import webdriver
from typing import Any
from rich import print
import time
from bs4 import BeautifulSoup


URL = "https://www.threads.com/"


def browsing() -> list[dict[str, Any]]:
    """
    瀏覽 Threads 平台並擷取貼文資訊

    參數:
        url: 特定的 Threads 頁面 URL，如果為 None 則使用預設首頁

    回傳:
        一個包含貼文資訊的字典清單，每個字典包含貼文 ID、作者、內容、時間等資訊
    """
    options = webdriver.ChromeOptions()
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

    posts_data: list[dict[str, Any]] = []

    try:
        # 前往 threads 頁面
        driver.get(URL)
        print(f"🌐 正在載入 threads 頁面: {URL}...")
        time.sleep(5)  # 等待頁面完全載入

        # 檢查是否成功載入
        if "threads.net" in driver.current_url or "threads.com" in driver.current_url:
            print("✅ 成功載入 threads 頁面")
        else:
            print("❌ 載入失敗，請檢查 URL")
            return [{"message": "Failed to load threads page"}]

        # 往下滑動
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # 取得目前的頁面 html，然後使用 soup 分析
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, "html.parser")

        # 找到所有貼文的容器
        post_containers = soup.find_all(
            "div", class_="x78zum5 xdt5ytf x1iyjqo2 x1n2onr6"
        )[1]

        print(f"找到 {len(post_containers)} 篇貼文")

        for post_container in post_containers:
            post_data = {
                "post_id": None,
                "user_id": None,
                "post_url": None,
                "text_content": None,
                "time_text": None,
                "time_text_from_now": None,
                "datetime": None,
                "like_count": None,
                "comment_count": None,
                "share_count": None,
                "images": None,  # 這邊會有多個，因為如果只有一張圖片會出現 media url 其他就是會有多個 image
                "avatar_url": None,
                "videos": None,
                "comments": None,  # 尚未實作
            }
            # 分析內容，加入到 posts_data
            hrefs = post_container.find_all("a", href=True)
            for href in hrefs:
                if "/post/" in href["href"]:
                    post_id = href["href"].split("/post/")[1]
                    post_id = post_id.split("/")[0]  # 避免多了 /media
                    user_id = href["href"].split("/@")[1].split("/")[0]
                    post_data["post_id"] = post_id
                    post_data["user_id"] = user_id
                    post_data["post_url"] = (
                        "https://threads.net/@" + user_id + "/post/" + post_id
                    )
                if "/@" in href["href"]:
                    user_id = href["href"].split("/@")[1].split("/")[0]
                    post_data["user_id"] = user_id

            if not post_data["post_id"]:
                continue

            # img and avatar
            images = post_container.find_all("img")
            if images:
                post_data["images"] = [
                    {image["src"]: image["alt"]} for image in images
                ][1:]
                post_data["avatar_url"] = images[0]["src"]

            # video
            videos = post_container.find_all("video")
            if videos:
                post_data["videos"] = [video["src"] for video in videos]

            # text content
            text_content = post_container.find(
                "span",
                class_="x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf xi7mnp6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xjohtrz xo1l8bm xp07o12 x1yc453h xat24cr xdj266r",
            )
            if text_content:
                post_data["text_content"] = text_content.text

            # time
            time_container = post_container.find("time")
            if time_container:
                post_data["time_text"] = time_container.get("title")
                post_data["datetime"] = time_container.get("datetime")
                post_data["time_text_from_now"] = time_container.text

            # 統計次數容器
            stats_container = post_container.find(
                "div", class_="x4vbgl9 xp7jhwk x1k70j0n"
            ).find("div", class_="x78zum5")
            for i, stat in enumerate(stats_container):
                state_number = stat.find("span", class_="x17qophe x10l6tqk x13vifvy")
                print(state_number)
                if state_number and state_number.text:
                    state_number = state_number.text
                else:
                    state_number = "0"
                if i == 0:
                    post_data["like_count"] = state_number
                if i == 1:
                    post_data["comment_count"] = state_number
                if i == 2:
                    post_data["repost_count"] = state_number
                if i == 3:
                    post_data["share_count"] = state_number

            posts_data.append(post_data)

    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        return [{"message": f"Error: {str(e)}"}]
    finally:
        # 關閉瀏覽器
        driver.quit()
        print("🔒 瀏覽器已關閉")

    return posts_data


if __name__ == "__main__":
    posts = browsing()
    print(posts)
