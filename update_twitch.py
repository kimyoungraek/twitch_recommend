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
    resp = requests.post(url, params=params)
    return resp.json().get("access_token")
def get_top_streams(num=5, lang=None):
    token = get_access_token()
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    params = {
        "first": num
    }
    if lang:
        params["language"] = lang   # 예시: "ko"면 한국어 방송
    resp = requests.get(url, headers=headers, params=params)
    streams = resp.json().get("data", [])
    result = []
    for stream in streams:
        user = stream["user_name"]
        title = stream["title"]
        viewers = stream["viewer_count"]
        game = stream.get("game_name", "Unknown")
        thumb = stream["thumbnail_url"].replace("{width}", "320").replace("{height}", "180")
        link = f"https://twitch.tv/{user}"
        # 썸네일과 정보 한 번에 마크다운으로
        entry = f"[![thumb]({thumb})]({link})\n**[{title}]({link})** by **{user}**<br>{viewers:,}명 시청  - {game}"
        result.append(entry)
    return result
def update_readme(streams):
    from datetime import datetime
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# : 실시간 트위치 시청자수 Top 5\n\n")
        for i, stream in enumerate(streams, 1):
            f.write(f"**{i}.** {stream}\n\n")
        f.write(f"\n---\n")
        f.write(f": 마지막 업데이트: {now}\n")
        f.write("\nPowered by [Twitch API](https://dev.twitch.tv/docs/api/reference) · 자동화 봇")
if __name__ == "__main__":
    streams = get_top_streams(num=5)
    update_readme(streams)
