# harmony_notifications.py
import requests

# Send message to an ntfy url, set custom priority or tags if required
def send_notification(send_url, message, title, tags, priority, auth_token):
    if send_url:
        headers = {
            "Title": title,
            "Priority": priority,
            "Tags": tags,
            "Authorization": f"Bearer {auth_token}"
        }
        response = requests.post(send_url, data=message, headers=headers)
        if response.status_code != 200:
            print(f"Failed to send notification: {response.status_code}")
