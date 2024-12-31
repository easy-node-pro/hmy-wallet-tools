# harmony_notifications.py
import requests

# Send message to an ntfy url, set custom priority or tags if required. Modify for anywhere you'd like to dump a notification.
def send_notification(send_url, message, title, priority = "normal", tags = "harmony,rewards"):
    if send_url:
        headers = {
            "X-Title": title,
            "X-Priority": priority,
            "X-Tags": tags
        }
        requests.post(f"{send_url}", data=message, headers=headers)
        print(f"Notification sent to {send_url}")