import requests
import os
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
    access_token = response.json().get("access_token")
    return access_token
def get_top_streams(token, num=5):
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    params = {
        "first": num,
        "language": "ko"  # 한국어 방송만 필터
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get("data", [])
    result = []
    for stream in data:
        user = stream["user_name"]
        title = stream["title"]
        viewers = stream["viewer_count"]
        game = stream["game_name"]
        thumb = stream["thumbnail_url"].replace("{width}", "160").replace("{height}", "90")
        link = f"https://twitch.tv/{user}"
        result.append(f"![thumb]({thumb})\n[{title}]({link}) by {user} ({viewers:,}명 시청) - {game}")
    return result
def update_readme(streams):
    from datetime import datetime
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open("README.md", "a", encoding="utf-8") as f:
        f.write("\n# :큰_보라색_원: 지금 인기 트위치 스트리머 Top 5\n\n")
        for i, stream in enumerate(streams, 1):
            f.write(f"**{i}.** {stream}\n\n")
        f.write(f"\n:모래가_내려오고_있는_모래시계: 마지막 업데이트: {now}\n")
        f.write("\nPowered by [Twitch API](https://dev.twitch.tv/docs/api/reference) · 자동화 봇")
if __name__ == "__main__":
    token = get_access_token()
    streams = get_top_streams(token, num=5)
    update_readme(streams)
