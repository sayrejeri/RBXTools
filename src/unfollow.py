import time
from datetime import datetime
import requests

print("RBXTools – Roblox Unfollow Manager")
print("----------------------------------")
print("This tool runs locally. Never share your .ROBLOSECURITY cookie.\n")

# ===== USER INPUT =====
roblox_id = int(input("Enter your Roblox User ID: ").strip())
cookie = input("Paste your .ROBLOSECURITY cookie: ").strip()

unfollow_non_friends_only = input("Unfollow non-friends only? (y/n): ").lower().startswith("y")
unfollow_offline_only = input("Unfollow offline users only? (y/n): ").lower().startswith("y")

DELAY_SECONDS = 0.25
# ======================

session = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie

session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.roblox.com/",
    "Origin": "https://www.roblox.com",
})

log_path = f"unfollowed_{roblox_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
log_file = open(log_path, "a", encoding="utf-8")

def ensure_csrf():
    r = session.post("https://friends.roblox.com/v1/users/1/unfollow")
    token = r.headers.get("x-csrf-token")
    if token:
        session.headers["x-csrf-token"] = token
        return True
    return False

def get_followings(cursor=None):
    params = {"sortOrder": "Asc", "limit": 100}
    if cursor:
        params["cursor"] = cursor
    r = session.get(f"https://friends.roblox.com/v1/users/{roblox_id}/followings", params=params)
    r.raise_for_status()
    return r.json()

def get_friend_statuses(user_ids):
    if not user_ids:
        return {}
    r = session.post(
        f"https://friends.roblox.com/v1/users/{roblox_id}/friends/statuses",
        json={"userIds": user_ids}
    )
    return {x["id"]: x["isFriend"] for x in r.json().get("data", [])}

def get_presence_statuses(user_ids):
    if not user_ids:
        return {}
    r = session.post(
        "https://presence.roblox.com/v1/presence/users",
        json={"userIds": user_ids}
    )
    return {x["userId"]: x["userPresenceType"] for x in r.json().get("userPresences", [])}

def get_usernames(user_ids):
    r = session.post(
        "https://users.roblox.com/v1/users",
        json={"userIds": user_ids, "excludeBannedUsers": False}
    )
    return {u["id"]: u["name"] for u in r.json().get("data", [])}

def unfollow(user_id):
    r = session.post(f"https://friends.roblox.com/v1/users/{user_id}/unfollow")
    if r.status_code == 403:
        ensure_csrf()
        r = session.post(f"https://friends.roblox.com/v1/users/{user_id}/unfollow")
    return r.status_code

if not ensure_csrf():
    print("Failed to obtain CSRF token. Cookie may be invalid.")
    exit(1)

print("\nStarting unfollow process...\n")

try:
    cursor = None
    while True:
        page = get_followings(cursor)
        users = page.get("data", [])
        if not users:
            break

        ids = [u["id"] for u in users]
        names = get_usernames(ids)
        friend_map = get_friend_statuses(ids) if unfollow_non_friends_only else {}
        presence_map = get_presence_statuses(ids) if unfollow_offline_only else {}

        for uid in ids:
            if unfollow_non_friends_only and friend_map.get(uid):
                continue

            if unfollow_offline_only and presence_map.get(uid) != 0:
                continue

            status = unfollow(uid)
            name = names.get(uid, str(uid))

            if status in (200, 204):
                print(f"Unfollowed: {name} ({uid})")
                log_file.write(f"{uid}\t{name}\n")
                log_file.flush()
            elif status == 429:
                print("Rate limited. Sleeping 10 seconds...")
                time.sleep(10)
            elif status == 401:
                raise RuntimeError("Authentication failed. Invalid cookie.")

            time.sleep(DELAY_SECONDS)

        cursor = page.get("nextPageCursor")
        if not cursor:
            break

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    log_file.close()
    print("\nSaved log to:", log_path)
    print("Done. Log out of Roblox to invalidate your cookie.")
