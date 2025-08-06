import requests
import os
# 환경변수에서 클라이언트 아이디와 시크릿을 읽음 (GitHub Secrets에 등록 필요)
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
def get_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    return response.json().get("access_token")
def get_top_streams(token, num=5, lang=None):
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    params = {
        "first": num
    }
    if lang:
        params["language"] = lang   # "ko" 넣으면 한국어 방송만!
    response = requests.get(url, headers=headers, params=params)
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
    from datetime import datetime
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open("README.md", "a", encoding="utf-8") as f:
        f.write("\n# :큰_보라색_원: 실시간 트위치 시청자수 Top 5\n\n")
        for i, stream in enumerate(streams, 1):
            f.write(f"**{i}.** {stream}\n\n")
        f.write(f"\n:모래가_내려오고_있는_모래시계: 마지막 업데이트: {now}\n")
        f.write("\nPowered by [Twitch API](https://dev.twitch.tv/docs/api/reference) · 자동화 봇")
if __name__ == "__main__":
    token = get_access_token()
    streams = get_top_streams(token, num=5)  # 한국어 방송만 보려면 num=5, lang="ko"
    update_readme(streams)
