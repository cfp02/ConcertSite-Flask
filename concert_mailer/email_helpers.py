from datetime import datetime
import os
import logging
from flask_mail import Mail, Message
from flask import current_app
from concert_mailer.db import get_concert, get_venue_by_id

email_subject_1 = "Photography inquiry for {{artist}} at {{venue}} on {{date_subject}}"
email_subject_2 = "Photography inquiry for {{artist}} at {{venue}} ({{date_subject}})"
email_subject_3 = "{{artist}} {{city}} Media Coverage ({{date_subject}})"

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

template_html_2 = """<!DOCTYPE html>
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
            <p>I'm Cole, a Boston-based photographer, and I've been fortunate enough to photograph some amazing concerts in the area. I saw that {{artist}} is performing at {{venue}} on {{date}} and I'd love to work together to capture the energy of the performance! I turn around all my work overnight or within 24 hours and I'm very flexible to work within any budget. I'm also potentially open to coming in to shoot for free.</p><br>
            <p>Here is a link to my website with some of my previous work: <a href="https://coleparksphotography.com/concerts">coleparksphotography.com/concerts</a></p>
            <p>Let me know what you think!</p><br>
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
    # Looks like 'Monday, January 1'
    normal_date = date.strftime("%A, %B %d")
    
    day_num = normal_date[-2:]
    # Add the appropriate suffix to the day number
    if day_num == '01' or day_num == '21' or day_num == '31':
        suffix = 'st'
    elif day_num == '02' or day_num == '22':
        suffix = 'nd'
    elif day_num == '03' or day_num == '23':
        suffix = 'rd'
    else:
        suffix = 'th'

    if normal_date[-2] == "0":
        normal_date = normal_date[:-2] + normal_date[-1]

    normal_date = normal_date + suffix

    return short_date, normal_date

def generate_concert_email(concert_id: int):
    '''
    Takes a concert ID and generates the formatted placeholders to be used in the email template.
    '''
    concert = get_concert(concert_id)
    
    mail_obj: Mail = current_app.extensions['mail']

    # concert['date'] is in the format 'YYYY-MM-DD'
    date_datetime = datetime.strptime(concert['date'], '%Y-%m-%d')

    

    date_subject, date = date_manipulation(date_datetime)
    print("Date is ", date)

    mgmt_name = 'there' if concert['mgmt_name'] == '' else concert['mgmt_name']

    venue = get_venue_by_id(concert['venue_id'])
    venue_name = venue['name']
    venue_email_text = venue['venue_email_text'] or venue_name  # Fallback to venue name if email text is not set


    placeholders = {
        'mgmt_name': mgmt_name,
        'artist': concert['artist'],
        'venue': venue_email_text,
        'location': '',
        'date': date,
        'date_subject': date_subject,
        'city': venue['city']
    }

    print(placeholders)
    
    # Using template 1 and subject 2
    new_mail_obj, msg = generate_email(mail_obj, [concert['mgmt_email']], template_html_2, placeholders, sender='Cole Parks Photography',subject=email_subject_3)

    return new_mail_obj, msg
    

def generate_email(
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

    return email_obj, msg


def send_email(email_obj: Mail, msg: Message) -> bool:

    # Send the email
    try:    
        email_obj.send(msg)
        return True
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise e
        return False
