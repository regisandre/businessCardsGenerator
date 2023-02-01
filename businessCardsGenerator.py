#!/usr/bin/env python3

# https://code-maven.com/create-images-with-python-pil-pillow
import os, sys, re, csv, argparse
from PIL import Image, ImageDraw, ImageFont

# Define the phone number prefix and email domain
voip_number_prefix = "+32 2 616 " # Phone number prefix
email_domain = "odoo.com" # Email domain

# Company logo and icons
try:
    # Open the logo image
    logo = Image.open('resources/images/logo.png', 'r')
except Exception as e:
    # Print an error message if the image cannot be opened
    print(f"Unable to open the image: {e}")

# Resize the logo image
logo = logo.resize((110, 35), Image.ANTIALIAS)

# Open and resize phone, mobile, email, map marker, and web icons
phone_icon = Image.open('resources/images/phone.png', 'r')
phone_icon = phone_icon.resize((24, 24), Image.ANTIALIAS)

mobile_icon = Image.open('resources/images/mobile.png', 'r')
mobile_icon = mobile_icon.resize((24, 24), Image.ANTIALIAS)

mail_icon = Image.open('resources/images/mail.png', 'r')
mail_icon = mail_icon.resize((24, 24), Image.ANTIALIAS)

map_marker_icon = Image.open('resources/images/map-marker.png', 'r')
map_marker_icon = map_marker_icon.resize((24, 24), Image.ANTIALIAS)

web_icon = Image.open('resources/images/web.png', 'r')
web_icon = web_icon.resize((24, 24), Image.ANTIALIAS)

# Fonts
fnt="resources/fonts/arial.ttf"
main_font = ImageFont.truetype(fnt, 26)
name_font = ImageFont.truetype(fnt, 44)
job_position_font = ImageFont.truetype(fnt, 32)

# Colors
main_color = 0, 0, 0
job_position_color = 135, 91, 124

# Define script arguments using argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='Path to input CSV file')
parser.add_argument('--output-directory', '-o', help='Path to output folder', required=True)
parser.add_argument('--fullname', '-fn', help="Full name", required=True)
parser.add_argument('--username', '-u', help="Username", required=True)
parser.add_argument('--jobposition', '-jp', help="Job title", required=True)
parser.add_argument('--voipnumberextension', '-pne', help="VoIP phone number extension without space (ex: 8269)")
parser.add_argument('--mobilenumber', '-mn', help="Mobile phone number")
parser.add_argument('--location', '-ol', help="Office location", choices=['LLN', 'ANT', 'GR1', 'GR2', 'GR3'], default='LLN', required=True)
parser.add_argument('--website', '-w', help="Website URL", default='www.odoo.com')
arguments = parser.parse_args()

# Function to generate business card
def generate_business_card(full_name, username, job_position, voip_number, mobile_number, office_location, website):
    # Global variables to store the work address
    global work_address_line_1
    global work_address_line_2
    
    # Determine the work address based on the office location
    if(office_location == "LLN"):
        work_address_line_1 = "Rue Laid Burniat 5"
        work_address_line_2 = "1348 Louvain-la-Neuve"
        work_address_line_3 = "BELGIUM"
    elif(office_location == "ANT"):
        work_address_line_1 = "Berchemstadionstraat 72"
        work_address_line_2 = "2600 Berchem"
        work_address_line_3 = "BELGIUM"
    elif(office_location == "GR1"):
        work_address_line_1 = "Chaussée de Namur 40"
        work_address_line_2 = "1367 Grand-Rosière"
        work_address_line_3 = "BELGIUM"
    elif(office_location == "GR2"):
        work_address_line_1 = "Rue des Bourlottes 9"
        work_address_line_2 = "1367 Grand-Rosière"
        work_address_line_3 = "BELGIUM"
    elif(office_location == "GR3"):
        work_address_line_1 = "Rue de Ramillies 1"
        work_address_line_2 = "1367 Grand-Rosière"
        work_address_line_3 = "BELGIUM"

    # Format username
    username == f"{username}@{email_domain}"

    # Create image object and image drawer object
    img = Image.new('RGB', (1050, 600), color = (255, 255, 255))
    business_card_image = ImageDraw.Draw(img)

    # Header (with company logo, full name, job title and a colored line)
    img.paste(logo, (79,98), logo) # https://stackoverflow.com/questions/2563822/how-do-you-composite-an-image-onto-another-image-with-pil-in-python
    business_card_image.text((255,88), full_name, font=name_font, fill=(main_color)) # Full name
    business_card_image.text((255,148), job_position, font=job_position_font, fill=(job_position_color)) # Job title
    business_card_image.line([(255,197), (1050,197)], fill=job_position_color, width = 3) # https://www.geeksforgeeks.org/python-pil-imagedraw-draw-line/

    # Contact information - icons and text
    info = {
        'voip_number': (phone_icon, voip_number),
        'mobile_number': (mobile_icon, mobile_number),
        'username': (mail_icon, username)
    }

    for i, (icon, text) in info.items():
        if text != '/' and text != '':
            img.paste(icon, (258, 225 + 34 * i), icon)
            business_card_image.text((299, 222 + 34 * i), text, font=main_font, fill=(main_color))

    """
    info = [    {        'icon': phone_icon,        'text': voip_number    },    {        'icon': mobile_icon,        'text': mobile_number    },    {        'icon': mail_icon,        'text': username    }]

    for i, (icon, text) in enumerate(info.values()):
    if text != '/' and text != '':
        img.paste(icon, (258, 225 + 34 * i), icon)
        business_card_image.text((299, 222 + 34 * i), text, font=main_font, fill=(main_color))
    """
    
    """
    # Contact informations
    if voip_number != '/' and voip_number != '':
        img.paste(phone_icon, (258,225), phone_icon)
        business_card_image.text((299,222), voip_number, font=main_font, fill=(main_color)) # Phone number
        if mobile_number != '/' and mobile_number != '':
            img.paste(mobile_icon, (258,259), mobile_icon)
            business_card_image.text((299,257), mobile_number, font=main_font, fill=(main_color)) # Mobile phone number
            if username != '/' and username != '':
                img.paste(mail_icon, (258, 293), mail_icon)
                business_card_image.text((299,288), username, font=main_font, fill=(main_color)) # Email
    else:
        if mobile_number != '/' and mobile_number != '':
            img.paste(mobile_icon, (258,225), mobile_icon)
            business_card_image.text((299,222), mobile_number, font=main_font, fill=(main_color)) # Mobile phone number
            if username != '/' and username != '':
                img.paste(mail_icon, (258, 293), mail_icon)
                business_card_image.text((299,288), username, font=main_font, fill=(main_color)) # Email
        elif username != '/' and username != '':
            img.paste(mail_icon, (258, 225), mail_icon)
            business_card_image.text((299,222), username, font=main_font, fill=(main_color)) # Email

    """

    """
    # Former code
    # Contact informations
    img.paste(phone_icon, (258,225), phone_icon)
    business_card_image.text((299,222), voip_number, font=main_font, fill=(main_color)) # Phone number

    if(mobile_number != '/' and mobile_number != ''):
        img.paste(mobile_icon, (258,259), mobile_icon)
        business_card_image.text((299,257), mobile_number, font=main_font, fill=(main_color)) # Mobile phone number
        img.paste(mail_icon, (258,293), mail_icon)
        business_card_image.text((299,288), username, font=main_font, fill=(main_color)) # Email
    else:
        img.paste(mail_icon, (258,259), mail_icon)
        business_card_image.text((299,257), username, font=main_font, fill=(main_color)) # Email
    """

    # Footer (with address and website)
    img.paste(map_marker_icon, (258,418), map_marker_icon)
    business_card_image.text((299,414), work_address_line_1, font=main_font, fill=(main_color)) # Address line 1
    business_card_image.text((299,446), work_address_line_2, font=main_font, fill=(main_color)) # Address line 2
    business_card_image.text((299,479), work_address_line_3, font=main_font, fill=(main_color)) # Address line 3 | Country
    img.paste(web_icon, (258,515), web_icon)
    business_card_image.text((299,511), website, font=main_font, fill=(main_color)) # Website

    # Create directories for saving the generated business card
    os.makedirs(f"{arguments.output_directory}", mode = 0o755, exist_ok = True)
    os.makedirs(f"{arguments.output_directory}/auto_generated_business-cards", mode = 0o755, exist_ok = True)

    # Save the generated business cards
    img.save(f"{arguments.output_directory}/auto_generated_business-cards/{username}_businessCard_verso.png")

# Check if file argument is provided, use it to generate business card variables, else use other arguments
if arguments.file:
    # Parse the CSV file to generate the variables
    with open(arguments.file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_header = next(csv_reader) # skip the header row - https://stackoverflow.com/questions/16350480/python-csv-reader-loop-from-the-second-row
        
        # Loop through each row of the CSV file
        for row in csv_reader:
            # Skip empty rows
            # https://stackoverflow.com/questions/855493/referenced-before-assignment-error-in-python
            if any(row):
                # Extract information from the row
                full_name = f"{row[2]} {row[1]}"
                username = row[0].lower()
                job_position = row[3]
                voip_number = row[4]
                mobile_number = row[5]
                location = row[6]
                website = row[7]
                # Generate business card with extracted information
                generate_business_card(full_name, username, job_position, voip_number, mobile_number, location, website)
    # Close the CSV file
    csv_file.close()
else:
    # Assign values to variables from arguments provided
    full_name = arguments.full_name
    username = arguments.username
    job_position = arguments.jobposition
    # Join every two characters in voip_number_extension with a space
    voip_number_extension = ' '.join(re.findall('..',arguments.voipnumberextension)) # https://stackoverflow.com/questions/9475241/split-string-every-nth-character & https://www.geeksforgeeks.org/python-convert-list-of-strings-to-space-separated-string/
    # Concatenate voip_number_prefix and voip_number_extension to form voip_number
    voip_number = f"{voip_number_prefix}{voip_number_extension}"
    mobile_number = arguments.mobilenumber
    location = arguments.location
    website = arguments.website

    # Call the generate_business_card function with the assigned variables
    generate_business_card(full_name, username, job_position, voip_number, mobile_number, location, website)
