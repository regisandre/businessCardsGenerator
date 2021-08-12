#!/usr/bin/env python3

# https://code-maven.com/create-images-with-python-pil-pillow
import os, sys, re, csv, argparse
from PIL import Image, ImageDraw, ImageFont

website = "www.odoo.com"

# Company logo and icons
logo = Image.open('resources/images/logo.png', 'r');
logo = logo.resize((110, 35), Image.ANTIALIAS)

phone_icon = Image.open('resources/images/phone.png', 'r');
phone_icon = phone_icon.resize((24, 24), Image.ANTIALIAS)

mobile_icon = Image.open('resources/images/mobile.png', 'r');
mobile_icon = mobile_icon.resize((24, 24), Image.ANTIALIAS)

mail_icon = Image.open('resources/images/mail.png', 'r');
mail_icon = mail_icon.resize((24, 24), Image.ANTIALIAS)

map_marker_icon = Image.open('resources/images/map-marker.png', 'r');
map_marker_icon = map_marker_icon.resize((24, 24), Image.ANTIALIAS)

web_icon = Image.open('resources/images/web.png', 'r');
web_icon = web_icon.resize((24, 24), Image.ANTIALIAS)

# Fonts
fnt="resources/fonts/arial.ttf"
main_font = ImageFont.truetype(fnt, 26)
name_font = ImageFont.truetype(fnt, 44)
job_title_font = ImageFont.truetype(fnt, 32)

# Colors
main_color = 0, 0, 0
job_title_color = 135, 91, 124

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='Path to input CSV file')
parser.add_argument('--output-directory', '-o', help='Path to output folder', required=True)
parser.add_argument('--fullname', help="Full name")
parser.add_argument('--username', help="Username")
parser.add_argument('--jobtitle', help="Job title")
parser.add_argument('--phonenumberextension', help="VoIP phone number extension without space (ex: 8167)")
parser.add_argument('--mobilephonenumber', help="Mobile phone number")
parser.add_argument('--location', help="Office location", choices=['LLN', 'ANT', 'GR1', 'GR2', 'GR3'], default='LLN')
arguments = parser.parse_args()

# Generating the image
def generateImage(fullname, username, job_title, phone_number, mobile_phone_number, work_location):
    # Work address
    global work_address_line_1
    global work_address_line_2
    if(work_location == "LLN"):
        work_address_line_1 = "Rue Laid Burniat 5"
        work_address_line_2 = "1348, Louvain-la-Neuve"
    elif(work_location == "ANT"):
        work_address_line_1 = "Berchemstadionstraat 72"
        work_address_line_2 = "2600, Berchem"
    elif(work_location == "GR1"):
        work_address_line_1 = "Chaussée de Namur 40"
        work_address_line_2 = "1367, Grand-Rosière"
    elif(work_location == "GR2"):
        work_address_line_1 = "Rue des Bourlottes 9"
        work_address_line_2 = "1367, Grand-Rosière"
    elif(work_location == "GR3"):
        work_address_line_1 = "Rue de Ramillies 1"
        work_address_line_2 = "1367, Grand-Rosière"

    img = Image.new('RGB', (1050, 600), color = (255, 255, 255))
    business_card_image = ImageDraw.Draw(img)

    # Header with company logo, full name, job title and a colored line
    img.paste(logo, (79,98), logo) # https://stackoverflow.com/questions/2563822/how-do-you-composite-an-image-onto-another-image-with-pil-in-python
    business_card_image.text((255,88), fullname, font=name_font, fill=(main_color)) # Full name
    business_card_image.text((255,148), job_title, font=job_title_font, fill=(job_title_color)) # Job title
    business_card_image.line([(255,197), (1050,197)], fill=job_title_color, width = 3) # https://www.geeksforgeeks.org/python-pil-imagedraw-draw-line/

    # Contact informations
    img.paste(phone_icon, (258,225), phone_icon)
    business_card_image.text((299,222), phone_number, font=main_font, fill=(main_color)) # Phone number

    if(mobile_phone_number != '/' and mobile_phone_number != ''):
        img.paste(mobile_icon, (258,255), mobile_icon)
        business_card_image.text((299,253), mobile_phone_number, font=main_font, fill=(main_color)) # Mobile phone number
        img.paste(mail_icon, (258,293), mail_icon)
        business_card_image.text((299,288), f"{username}@odoo.com", font=main_font, fill=(main_color)) # Email
    else:
        img.paste(mail_icon, (258,260), mail_icon)
        business_card_image.text((299,255), f"{username}@odoo.com", font=main_font, fill=(main_color)) # Email

    # Footer
    img.paste(map_marker_icon, (258,418), map_marker_icon)
    business_card_image.text((299,414), work_address_line_1, font=main_font, fill=(main_color)) # Address line 1
    business_card_image.text((299,446), work_address_line_2, font=main_font, fill=(main_color)) # Address line 2
    img.paste(web_icon, (258,483), web_icon)
    business_card_image.text((299,479), website, font=main_font, fill=(main_color)) # Odoo website

    # Create all needed directories
    os.makedirs(f"{arguments.output_directory}", mode = 0o755, exist_ok = True)
    os.makedirs(f"{arguments.output_directory}/auto_generated_business-cards", mode = 0o755, exist_ok = True)

    # Save the auto generated business card image
    img.save(f"{arguments.output_directory}/auto_generated_business-cards/{username}_businessCard_verso.png")

if arguments.file:
    # Parse the CSV file to generate the variables
    with open(arguments.file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_header = next(csv_reader) # https://stackoverflow.com/questions/16350480/python-csv-reader-loop-from-the-second-row
        for row in csv_reader:
            # Check if row is empty - https://stackoverflow.com/questions/855493/referenced-before-assignment-error-in-python
            if any(row):
                fullname = f"{row[1]} {row[2]}"
                username = row[0].lower()
                job_title = row[3]
                phone_number = row[4]
                mobile_phone_number = row[5]
                location = row[6]
                generateImage(fullname, username, job_title, phone_number, mobile_phone_number, location)
    csv_file.close();
else:
    fullname = arguments.fullname
    username = arguments.username
    job_title = arguments.jobtitle
    phone_number_extension = ' '.join(re.findall('..',arguments.phonenumberextension)) # https://stackoverflow.com/questions/9475241/split-string-every-nth-character & https://www.geeksforgeeks.org/python-convert-list-of-strings-to-space-separated-string/
    phone_number = f"+32 2 616 {phone_number_extension}"
    mobile_phone_number = arguments.mobilephonenumber
    location = arguments.location
    generateImage(fullname, username, job_title, phone_number, mobile_phone_number, location)