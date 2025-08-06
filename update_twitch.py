import requests
import os
from datetime import datetime

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

def get_access_token():
    """Twitch Access Token 발급"""
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]

def get_top_game_streams(token, num=5, lang="ko"):
    """게임 카테고리 스트림만 가져오기"""
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    params = {"first": 20, "language": lang}  # 여유 있게 20개 가져와서 게임만 추려냄
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json().get("data", [])

    result = []
    for stream in data:
        game = stream.get("game_name", "Unknown")
        if game.lower() == "just chatting":
            continue  # 게임이 아닌 'Just Chatting' 카테고리 제외

        user = stream["user_name"]
        title = stream["title"]
        viewers = stream["viewer_count"]
        thumb = stream["thumbnail_url"].replace("{width}", "160").replace("{height}", "90")
        link = f"https://twitch.tv/{user}"
        result.append(f"![thumb]({thumb})\n[{title}]({link}) by {user} ({viewers:,}명 시청) - {game}")

        if len(result) == num:
            break  # 원하는 개수만큼 추출 후 종료

    return result

def update_readme(streams):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    content = f
