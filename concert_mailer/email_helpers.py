from datetime import datetime
import os
import logging
from flask_mail import Mail, Message

email_subject_1 = "Photography inquiry for {{artist}} at {{venue}} on {{date_subject}}"
email_subject_2 = "Photography inquiry for {{artist}} at {{venue}} ({{date_subject}})"

template_html_1 = """<!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    font-size: 13px; /* This is a typical 'normal' size, adjust as needed */
                }
                p {
                    margin: 0 0 0px 0; /* Adjust paragraph spacing */
                }
                .signature {
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <p>Hi {{mgmt_name}}!</p><br>
            <p>I'm Cole, and I'm reaching out to see if you are in need of photography services for {{artist}}'s performance at {{venue}} {{location}}on {{date}}. I'd love to come out and take photos!</p><br>
            <p>Here is a link to my website with some of my previous work: <a href="https://coleparksphotography.com/concerts">coleparksphotography.com/concerts</a></p>
            <p>Thank you in advance for your consideration!</p><br>
            <p>Best,<br>
            <p class="signature">
            Cole Parks<br>
            <a href="https://coleparksphotography.com">coleparksphotography.com</a></p>
            <p>&nbsp;</p>
        </body>
        </html>"""

def replace_placeholders(template_body: str, placeholders: dict[str, str]) -> str:
    '''
    Replaces placeholders in the template HTML with the appropriate values. 
    Keys in the template HTML should be surrounded by double curly braces, e.g. {{key}}.

    Args:
    template_body (str): The template HTML to replace placeholders in
    placeholders (dict): A dictionary of placeholders and their values

    Returns:
        template_body (str): The template HTML with placeholders replaced with their values
    '''
    for key, value in placeholders.items():
        template_body = template_body.replace("{{" + key + "}}", value)
    return template_body

def date_manipulation(date: datetime):
    # Looks like 'Jan 1'
    short_date = date.strftime("%b %d")
    if short_date[-2] == "0":
        short_date = short_date[:-2] + short_date[-1]
    # Looks like 'Monday, January 01'
    normal_date = date.strftime("%A, %B %d")
    return short_date, normal_date

def send_email(
    email_obj: Mail,
    recipients: list[str],
    template_body: str,
    placeholders: dict[str, str],
    sender = 'Cole Parks Photography',
    subject: str = "Photography inquiry for {{artist}} at {{venue}} on {{date_subject}}",
):
    # Replace template html with placeholders
    replaced_body = replace_placeholders(template_body, placeholders)
    replaced_subject = replace_placeholders(subject, placeholders)

    # Create message object
    msg = Message(replaced_subject, recipients=recipients, sender=sender)

    # Set the body of the email, if it begins with HTML tags treat it as HTML, otherwise treat it as plain text
    if replaced_body.startswith('<'):
        msg.html = replaced_body
    else:
        msg.body = replaced_body

    # Send the email
    try:    
        email_obj.send(msg)
        return True
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise e
        return False
