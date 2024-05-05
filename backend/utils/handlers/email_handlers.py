import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings


def send_email(subject: str, body: str, recipient: str):

    html_template = """
        <!DOCTYPE html>
        <html lang="en">
            <head>
              <meta charset="UTF-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <title>Your Brand - OTP Verification</title>
              <style>
                body {
                      font-family: sans-serif;
                      margin: 0;
                      padding: 0;
                      background-color: #f5f5f5;
                    }
            
                    .container {
                      max-width: 600px;
                      padding: 30px;
                      margin: 0 auto;
                      background-color: #fff;
                      border-radius: 5px;
                      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
            
                    .header {
                      text-align: center;
                      padding-bottom: 20px;
                      border-bottom: 1px solid #ddd;
                    }
            
                    .header img {
                      width: 150px;
                    }
            
                    .content {
                      padding: 20px;
                    }
            
                    .content h1 {
                      font-size: 24px;
                      margin-bottom: 10px;
                    }
            
                    .otp-code {
                      display: flex;
                      justify-content: center;
                      margin: 20px 0;
                      padding: 10px;
                      background-color: #eee;
                      border-radius: 5px;
                    }
            
                    .otp-code-span {
                      font-size: 20px;
                      font-weight: bold;
                    }
            
                    .footer {
                      text-align: center;
                      padding-top: 20px;
                      border-top: 1px solid #ddd;
                    }
            
              </style>
            </head>
            <body>
              <div class="container">
                <header class="header">
                  <img src="logo.png" alt="Your Brand Logo">
                </header>
                <main class="content">
                  <h1>Welcome to Your Brand!</h1>
                  <p>To verify your account, please enter the following One-Time Password (OTP):</p>
                  <div class="otp-code">
                    <span class="otp-code-span">** [OTP] **</span>
                  </div>
                  <p>This OTP is valid for 5 minutes.</p>
                </main>
                <footer class="footer">
                  <p>If you didn't request this OTP, please ignore this email.</p>
                  <p>Regards,</p>
                  <p>The Your Brand Team</p>
                </footer>
              </div>
            </body>
        </html>
    """

    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    sender_email = settings.EMAIL_HOST_USER
    sender_password = settings.EMAIL_HOST_PASSWORD

    # Create a multipart message and set headers
    # message = MIMEMultipart()
    message = MIMEMultipart("alternative")
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject

    # Add body to email
    # message.attach(MIMEText(body, 'plain'))

    # Attach HTML template to the email
    html_body = html_template.replace("[OTP]", body)
    message.attach(MIMEText(html_body, 'html'))

    status = 0
    # Create SMTP session for sending the mail
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message.as_string())
        status = 1
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
        status = 0
    finally:
        server.quit()
        return status
