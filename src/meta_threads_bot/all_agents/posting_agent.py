import os

from agents import Agent, function_tool, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from dotenv import load_dotenv

from meta_threads_bot.Context.basic import PostContent
from meta_threads_bot.api import post_to_threads as post_to_threads_api
from meta_threads_bot.api import login_to_threads as login_to_threads_api

load_dotenv()


@function_tool(
    description_override="發文到 Threads，請提供貼文內容，如果需要登入，請提供 cookies 資訊"
)
def post_to_threads(
    context: RunContextWrapper[PostContent],
    caption: str,
) -> dict[str, str | int]:
    """Post to Threads"""

    if (
        not context.context.csrf_token
        or not context.context.session_id
        or not context.context.ds_user_id
    ):
        return {"message": "請先登入 Threads"}

    response = post_to_threads_api(
        caption=caption,
        csrf_token=context.context.csrf_token,
        session_id=context.context.session_id,
        ds_user_id=context.context.ds_user_id,
    )

    try:
        response_json = response.json()
        status = response_json.get("status", "unknown")

        if status == "ok":
            return {
                "message": "貼文已發文成功",
                "status": status,
                "response_text": (
                    response.text[:100] + "..."
                    if len(response.text) > 100
                    else response.text
                ),
            }
        else:
            return {
                "message": f"貼文失敗，狀態: {status}",
                "status": status,
                "response_text": (
                    response.text[:100] + "..."
                    if len(response.text) > 100
                    else response.text
                ),
            }
    except Exception as e:
        return {
            "message": f"貼文處理時發生錯誤: {str(e)}",
            "status_code": response.status_code,
            "response_text": (
                response.text[:100] + "..."
                if len(response.text) > 100
                else response.text
            ),
        }


@function_tool(
    description_override="使用帳號密碼登入 Threads 取得必要的 cookies 資訊，包含 csrftoken、sessionid 和 ds_user_id"
)
async def login_to_threads(
    context: RunContextWrapper[PostContent],
    username: str,
    password: str,
) -> dict[str, str]:
    context.context.username = username
    context.context.password = password
    cookies = login_to_threads_api(username, password)

    # 檢查 cookies 是否為 None
    if cookies is None:
        return {"message": "登入失敗，請提供正確的帳號密碼或者換網路再試一次"}

    if cookies.get("message") != "ok":
        return {"message": "登入失敗，請提供正確的帳號密碼或者換網路再試一次"}

    # 安全地取得 cookies 值
    csrf_token = cookies.get("csrftoken")
    session_id = cookies.get("sessionid")
    ds_user_id = cookies.get("ds_user_id")

    # 更新 context
    if csrf_token is not None:
        context.context.csrf_token = csrf_token
    if session_id is not None:
        context.context.session_id = session_id
    if ds_user_id is not None:
        context.context.ds_user_id = ds_user_id

    return {"message": "成功登入，已取得 cookies 資訊，並儲存到 context 中"}


@function_tool(description_override="檢查環境變數是否提供登入帳號密碼")
async def check_login() -> dict[str, str | None]:
    if not os.getenv("THREADS_USERNAME") or not os.getenv("THREADS_PASSWORD"):
        return {"message": "請先登入 Threads"}
    return {
        "message": "已經登入 Threads",
        "username": os.getenv("THREADS_USERNAME"),
        "password": os.getenv("THREADS_PASSWORD"),
    }


agent = Agent[PostContent](
    name="Posting Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    將使用者提供的貼文內容用工具發文到 Threads，如果有需要登入，請使用者提供密碼
    請先檢查使用者是否提供帳號密碼在環境變數。""",
    model="gpt-4o-mini",
    # handoff_description="負責登入並且發文到 Threads 的 Agent",
    handoff_description="帳號相關操作的 Agent",
    tools=[post_to_threads, login_to_threads, check_login],
)
