"""Sending the one email this application sends: a password reset code.

Deliberately smtplib from the standard library rather than a mail package.
One plain-text message to one recipient needs nothing more, and the settings
live in the environment so the sending account can change without a code
change -- a Gmail address today, an institutional one if the university enables
authenticated SMTP on its Microsoft tenant.

Note on the From address: it cannot be chosen freely. A domain's SPF record
says which servers may send as it, so sending as an @rupp.edu.kh address
through Gmail would fail that check and be treated as spoofing. Send as an
address belonging to whoever is authenticating.
"""
import os
import smtplib
import ssl
from email.message import EmailMessage

TIMEOUT = 15


def settings():
    return {
        "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "user": os.getenv("SMTP_USER", "").strip(),
        "password": os.getenv("SMTP_PASSWORD", ""),
        "sender": os.getenv("SMTP_FROM", "").strip(),
    }


def configured():
    """Whether a reset email could actually be sent.

    The sign-in screen asks this before offering "I forgot my password", so a
    deployment without mail does not show a door that leads nowhere.
    """
    s = settings()
    return bool(s["user"] and s["password"])


def send(to, subject, body):
    """Send one plain-text message. Raises on failure; the caller decides.

    App passwords are 16 characters that Google displays in groups of four,
    and they are pasted with the spaces more often than not. Google accepts
    either, but only if the string is otherwise intact, so the spaces are
    stripped here rather than left to fail as a wrong password.
    """
    s = settings()
    if not configured():
        raise RuntimeError("SMTP is not configured: set SMTP_USER and SMTP_PASSWORD.")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = s["sender"] or s["user"]
    message["To"] = to
    message.set_content(body)

    with smtplib.SMTP(s["host"], s["port"], timeout=TIMEOUT) as server:
        server.starttls(context=ssl.create_default_context())
        server.login(s["user"], s["password"].replace(" ", ""))
        server.send_message(message)


def reset_email(name, code, minutes):
    """The message body. Plain text on purpose: it renders everywhere, cannot
    carry a tracking pixel, and gives a phishing filter nothing to dislike."""
    return (
        f"Hello {name},\n\n"
        f"Use this code to set a new password for your Entrance Prep account:\n\n"
        f"    {code}\n\n"
        f"It expires in {minutes} minutes and can be used once.\n\n"
        f"If you did not ask to reset your password, you can ignore this email. "
        f"Your password has not changed.\n\n"
        f"Mechanical Engineering, Faculty of Engineering\n"
        f"Royal University of Phnom Penh\n"
    )
