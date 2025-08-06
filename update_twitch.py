import requests
import os
from datetime import datetime

# 환경 변수에서 클라이언트 정보 불러오기
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
    return response.json().get("access_token")

def get_top_streams(token, num=5, lang="ko"):
    """인기 스트림 Top N 가져오기"""
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    params = {"first": num, "language": lang}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json().get("data", [])
    result = []
    for stream in data:
        user = stream["user_name"]
        title = stream["title"]
        viewers = stream["viewer_count"]
        game = stream.get("game_name", "Unknown")
        thumb = stream["thumbnail_url"].replace("{width}", "160").replace("{height}", "90")
        link = f"https://twitch.tv/{user}"
        result.append(f"![thumb]({thumb})\n[{title}]({link}) by {user} ({viewers:,}명 시청) - {game}")
    return result

def update_readme(streams):
    """README.md 업데이트"""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    content = f"# 🎮 지금 인기 트위치 스트리머 Top 5\n\n"
    for i, stream in enumerate(streams, 1):
        content += f"**{i}.** {stream}\n\n"
    content += f"⏰ 마지막 업데이트: {now}\n\n"
    content += "Powered by [Twitch API](https://dev.twitch.tv/docs/api/reference) · 자동화 봇"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ README.md 업데이트 완료")

if __name__ == "__main__":
    token = get_access_token()
    streams = get_top_streams(token, num=5, lang="ko")
    update_readme(streams)
