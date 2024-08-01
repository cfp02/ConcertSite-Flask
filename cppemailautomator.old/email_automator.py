
import datetime
import os
import webbrowser
import csv

INPUT_DATA = "input_data"
OUTPUT_DATA = "output_data"

class ConcertDetails:
    def __init__(self, band_name, venue, concert_date: datetime.date, contact_name, contact_email):
        self.band_name = band_name
        self.venue = venue
        self.concert_date = concert_date
        self.concert_date_str_no_zero = concert_date.strftime("%Y-%m-%d")
        
        self.contact_name = contact_name
        self.contact_email = contact_email

        self.html = self.write_html()

    def __str__(self):
        return f"ConcertDetails({self.band_name}, {self.venue}, {self.concert_date}, {self.contact_name}, {self.contact_email})"

    def __eq__(self, other):
        return self.band_name == other.band_name and self.venue == other.venue and self.concert_date == other.concert_date and self.contact_name == other.contact_name and self.contact_email == other.contact_email

    def __hash__(self):
        return hash((self.band_name, self.venue, self.concert_date, self.contact_name, self.contact_email))

    def write_html(self):
        this_html = write_html_using_template(self.band_name, self.venue, self.concert_date, self.contact_name)
        return this_html

    def save_html(self, filename = ''):
        # Append by default
        mode = 'a'

        if filename == '':
            filename = f"{self.band_name}_{self.venue}_{self.concert_date.strftime('%Y-%m-%d')}.html"
            mode = 'w'

        filepath = os.path.join(OUTPUT_DATA, filename)

        with open(filepath, mode) as file:
            file.write(self.html)
        
        print("Wrote email to HTML successfully:", self.band_name, "at", self.venue, "on", self.concert_date.strftime("%Y-%m-%d"))

def write_html_using_template(band_name, venue, date: datetime.date, contact_name, location = "", year:bool=False):
    # Formatting the date in the desired format (e.g., Jul 20, 2024)
    if year:
        short_date = date.strftime("%b %d, %Y")
        normal_date = date.strftime("%A, %B %d, %Y")
    else:
        short_date = date.strftime("%b %d")
        if short_date[-2] == "0":
            short_date = short_date[:-2] + short_date[-1]
        normal_date = date.strftime("%A, %B %d")

    # If no contact name is provided, use "there" instead for "Hi there!"
    if contact_name == "":
        contact_name = "there"

    # If no location is provided, don't include it in the email
    if location != "":
        location = location + " "


    subject = f"Photography Inquiry for {band_name} at {venue} ({short_date})"
    # Add tab character so when it is pasted the cursor goes to the next entry box
    subject = subject + "\t"

    # Reading in the template HTML file
    with open("email_template.html", "r") as file:
        email_template = file.read()

    # Replacing the placeholders in the template HTML with the appropriate values
    email_template = email_template.replace("{{subject}}", subject)
    email_template = email_template.replace("{{band_name}}", band_name)
    email_template = email_template.replace("{{venue}}", venue)
    email_template = email_template.replace("{{date}}", normal_date)
    email_template = email_template.replace("{{contact_name}}", contact_name)
    email_template = email_template.replace("{{location}}", location)

    return email_template

def save_template_html():

    template_html = """<!DOCTYPE html>
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
            <p>{{subject}}</p>
            <p>&nbsp;</p>
            <p>Hi {{contact_name}}!</p><br>
            <p>I'm Cole, and I'm reaching out to see if you are in need of photography services for {{band_name}}'s performance at {{venue}} {{location}}on {{date}}. I'd love to come out and take photos!</p><br>
            <p>Here is a link to my website with some of my previous work: <a href="https://coleparksphotography.com/concerts">coleparksphotography.com/concerts</a></p>
            <p>Thank you in advance for your consideration!</p><br>
            <p>Best,<br>
            <p class="signature">
            Cole Parks<br>
            <a href="https://coleparksphotography.com">coleparksphotography.com</a></p>
            <p>&nbsp;</p>
            <p>----------------------------------------------------------------------------------------------------------------------------</p>
            <br>
        </body>
        </html>"""
    
    with open("email_template.html", "w") as file:
        file.write(template_html)
    
    print("Template HTML file created successfully.")

def save_email_to_html(band_name, venue, date, html, filename = ''):
    if filename == '':
        filename = f"{band_name}_{venue}_{date.strftime('%Y-%m-%d')}.html"

    with open(filename, "w") as file:
        file.write(html)
    
    print("Wrote email to HTML successfully:", band_name, "at", venue, "on", date.strftime("%Y-%m-%d"))

def read_csv_for_emails(csv_filename) -> list[ConcertDetails]:

    venue_row_name = "Venue"
    band_row_name = "Band Name"
    date_row_name = "Concert Date"
    contact_row_name = "Contact Name"
    contact_emamil_row_name = "Contact Email"

    concert_list = []

    filepath = os.path.join(INPUT_DATA, csv_filename)

    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            band_name = row[band_row_name]
            venue = row[venue_row_name]
            date = datetime.datetime.strptime(row[date_row_name], "%m/%d/%Y").date() if row[date_row_name] != "" else None
            contact_name = row[contact_row_name]
            contact_email = row[contact_emamil_row_name]
            # Make sure it's not a blank row
            if band_name != "":
                concert_list.append(ConcertDetails(band_name, venue, date, contact_name, contact_email))
    
    return concert_list

def make_html_from_csv(csv_filename, html_filename = '', open_html = False):
    
    save_template_html()
    concerts = read_csv_for_emails(csv_filename)
    if len(concerts) == 0:
        print("No concerts found in CSV file.")
        return
    if html_filename == '':
        html_filename = f"{csv_filename[:-4]}.html"
        # if that file already exists, append a number to the end
        i = 1
        while os.path.isfile(html_filename):
            html_filename = f"{csv_filename[:-4]}_{i}.html"
            i += 1

    for concert in concerts:
        concert.save_html(filename=html_filename)

    if open_html:
        path = os.path.join(OUTPUT_DATA, html_filename)
        webbrowser.open(path)


if __name__ == "__main__":
    make_html_from_csv('January24-Concerts.csv', open_html=True)

    
