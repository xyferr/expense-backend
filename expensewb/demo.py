import smtplib

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()  # Only if using TLS
    server.login("star080war@gmail.com", "okleodpxszmgsztn")
    server.sendmail("from@example.com", "xyf.no.69@gmail.com", "Subject: Test\n\nThis is a test email.")
    print("Email sent successfully.")
