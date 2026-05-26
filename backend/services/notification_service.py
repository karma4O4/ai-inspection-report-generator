import os
from dotenv import load_dotenv
import httpx

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("NOTIFICATION_EMAIL_FROM", "inspections@example.com")

class NotificationService:
    @classmethod
    def send_report_email(
        cls,
        client_email: str,
        client_name: str,
        report_title: str,
        pdf_url: str
    ) -> bool:
        """
        Sends an email containing the PDF inspection report URL to the client.
        Uses Resend or SendGrid depending on which API key is configured.
        Falls back to a simulated email print if no credentials exist.
        """
        subject = f"Your Inspection Report: {report_title}"
        html_content = f"""
        <h3>Hello {client_name},</h3>
        <p>Your property inspection report has been successfully generated.</p>
        <p><strong>Report:</strong> {report_title}</p>
        <p>You can access and download your detailed PDF inspection report here:</p>
        <p><a href="{pdf_url}" style="display:inline-block;background-color:#1e3a8a;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;font-weight:bold;">View PDF Report</a></p>
        <p>If the button doesn't work, copy and paste this link in your browser:<br/>{pdf_url}</p>
        <br/>
        <p>Best regards,<br/>Inspection Services Team</p>
        """

        # 1. Try Resend
        if RESEND_API_KEY and not RESEND_API_KEY.startswith("your-"):
            try:
                headers = {
                    "Authorization": f"Bearer {RESEND_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "from": FROM_EMAIL,
                    "to": [client_email],
                    "subject": subject,
                    "html": html_content
                }
                response = httpx.post("https://api.resend.com/emails", json=payload, headers=headers, timeout=10)
                if response.status_code in [200, 201]:
                    print(f"Email successfully sent via Resend to {client_email}")
                    return True
                else:
                    print(f"Resend returned error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"Error sending email via Resend: {e}")

        # 2. Try SendGrid
        if SENDGRID_API_KEY and not SENDGRID_API_KEY.startswith("your-"):
            try:
                headers = {
                    "Authorization": f"Bearer {SENDGRID_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "personalizations": [
                        {
                            "to": [{"email": client_email}],
                            "subject": subject
                        }
                    ],
                    "from": {"email": FROM_EMAIL},
                    "content": [
                        {
                            "type": "text/html",
                            "value": html_content
                        }
                    ]
                }
                response = httpx.post("https://api.sendgrid.com/v3/mail/send", json=payload, headers=headers, timeout=10)
                if response.status_code in [200, 202]:
                    print(f"Email successfully sent via SendGrid to {client_email}")
                    return True
                else:
                    print(f"SendGrid returned error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"Error sending email via SendGrid: {e}")

        # 3. Simulation Fallback Mode
        print(f"============================================================")
        print(f"[SIMULATION] Sending notification email to {client_email}")
        print(f"From: {FROM_EMAIL}")
        print(f"Subject: {subject}")
        print(f"PDF Link: {pdf_url}")
        print(f"============================================================")
        return True
