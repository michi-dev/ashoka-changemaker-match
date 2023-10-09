import smtplib
from email.mime.text import MIMEText

# Email configuration
sender_email = "test@michaelschaedler.li"

# SMTP server configuration (for Gmail)
smtp_server = 'asmtp.mail.hostpoint.ch'
smtp_port = 587
smtp_username = 'test@michaelschaedler.li'
smtp_password = 'b8p5hjSVY5isb&$!'

def sendmail(receiver_email, subject, message):
    msg = MIMEText(message, 'html')
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(smtp_username, smtp_password)  # Login to your email account

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Print a message indicating that the email was sent successfully
        print("Email sent successfully to " + receiver_email)

    except Exception as e:
        print(f"Email could not be sent. Error: {str(e)}")

    finally:
        server.quit()  # Quit the SMTP server
