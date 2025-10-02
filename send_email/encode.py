import base64

with open("logo.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

print(encoded[:200])  # potongan string base64
