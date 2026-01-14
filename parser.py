import email
import hashlib
import re
from email import policy

def parse_email(raw_email):
    msg = email.message_from_string(raw_email, policy=policy.default)

    headers = {
        "From": msg.get("From"),
        "To": msg.get("To"),
        "Subject": msg.get("Subject"),
        "Date": msg.get("Date"),
        "Message-ID": msg.get("Message-ID")
    }

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_content()
    else:
        body = msg.get_content()

    urls = re.findall(r'https?://\S+', body)
    sha256_hash = hashlib.sha256(raw_email.encode()).hexdigest()

    return {
        "headers": headers,
        "body": body,
        "urls": urls,
        "hash": sha256_hash
    }
