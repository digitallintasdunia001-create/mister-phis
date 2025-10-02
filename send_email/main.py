import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Data akun Hostinger
sender_email = "support@meditech.id"
sender_password = "C$zbp[l4"  # password email yang dibuat di hPanel
receiver_email = "2110511165@mahasiswa.upnvj.ac.id"

# Baca file HTML
with open("email6.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Buat pesan email
msg = MIMEMultipart("alternative")
msg["Subject"] = "Dari Login"
msg["From"] = f"Fulan Bin Fulan <{sender_email}>"
msg["To"] = receiver_email

# Versi plain text (fallback)
text = "Jika tidak terbaca HTML, tampilkan teks ini."

# Attach isi
msg.attach(MIMEText(text, "plain"))
msg.attach(MIMEText(html_content, "html"))

# Kirim via SMTP Hostinger
with smtplib.SMTP_SSL("smtp.hostinger.com", 465) as server:  # gunakan SSL port 465
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

print("✅ Email HTML dari file berhasil dikirim via Hostinger!")
