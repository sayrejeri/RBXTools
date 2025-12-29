import time
from datetime import datetime
import requests

print("RBXTools – Roblox Unfollow Tool")
print("--------------------------------")
print("This tool unfollows ALL users you are following.")
print("Runs locally. Never share your .ROBLOSECURITY cookie.\n")

# ===== USER INPUT =====
roblox_id = int(input("Enter your Roblox User ID: ").strip())
cookie = input("Paste your .ROBLOSECURITY cookie: ").strip()
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
    r = session.get(
        f"https://friends.roblox.com/v1/users/{roblox_id}/followings",
        params=params
    )
    r.raise_for_status()
    return r.json()

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

        for u in users:
            uid = u["id"]
            status = unfollow(uid)

            if status in (200, 204):
                print(f"Unfollowed user ID: {uid}")
                log_file.write(f"{uid}\n")
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
