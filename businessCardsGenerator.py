#!/usr/bin/env python3

# https://code-maven.com/create-images-with-python-pil-pillow
import os, sys, re, csv
from PIL import Image, ImageDraw, ImageFont

"""
name = sys.argv[1]
username = sys.argv[2]
jobTitle = sys.argv[3]
phoneNumberExtension = ' '.join(re.findall('..',sys.argv[4])) # https://stackoverflow.com/questions/9475241/split-string-every-nth-character & https://www.geeksforgeeks.org/python-convert-list-of-strings-to-space-separated-string/
phoneNumber = f"+32 2  616 {phoneNumberExtension}"
mobilePhoneNumber = sys.argv[5]
workAddressLine1 = "Rue Laid Burniat, 5" # Multiline text : https://www.geeksforgeeks.org/python-pil-imagedraw-draw-multiline_text/
workAddressLine2 = "1348,  Louvain-la-Neuve"
odooWebsite = "www.odoo.com"
"""

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        name = f"{row[1]} {row[2]}"
        username = row[0].lower()
        jobTitle = row[3]
        phoneNumber = row[4]
        mobilePhoneNumber = row[5]
        if(sys.argv[3] == "LLN"):
            workAddressLine1 = "Rue Laid Burniat 5"
            workAddressLine2 = "1348,  Louvain-la-Neuve"
        elif(sys.argv[3] == "ANT"):
            workAddressLine1 = "Berchemstadionstraat 72"
            workAddressLine2 = "2600, Berchem"
        elif(sys.argv[3] == "GR1"):
            workAddressLine1 = "Chaussée de Namur 40"
            workAddressLine2 = "1367, Grand-Rosière"
        elif(sys.argv[3] == "GR2"):
            workAddressLine1 = "Rue des Bourlottes 9"
            workAddressLine2 = "1367, Grand-Rosière"
        odooWebsite = "www.odoo.com"

        img = Image.new('RGB', (333, 219), color = (255, 255, 255)) # Image.open(r"pathToImageFile.png") 266, 175
        odooLogo = Image.open('resources/images/odooLogo.png', 'r');
        odooLogo = odooLogo.resize((35, 11), Image.ANTIALIAS)


        fnt="resources/fonts/arial.ttf"
        mainFont = ImageFont.truetype(fnt, 9)
        nameFont = ImageFont.truetype(fnt, 15)
        jobTitleFont = ImageFont.truetype(fnt, 11)

        mainColor = 0, 0, 0
        jobTitleColor = 135, 91, 124

        businessCardImage = ImageDraw.Draw(img)

        img.paste(odooLogo, (25,36), odooLogo) # https://stackoverflow.com/questions/2563822/how-do-you-composite-an-image-onto-another-image-with-pil-in-python
        businessCardImage.text((81,32), name, font=nameFont, fill=(mainColor)) # Name
        businessCardImage.text((81,52), jobTitle, font=jobTitleFont, fill=(jobTitleColor)) # Job title
        businessCardImage.line([(81,72), (308,72)], fill=jobTitleColor, width = 1) # https://www.geeksforgeeks.org/python-pil-imagedraw-draw-line/

        businessCardImage.text((82,80), f"Tel: {phoneNumber}", font=mainFont, fill=(mainColor)) # Phone number
        if(mobilePhoneNumber != "/"):
            businessCardImage.text((82,91), f"Mobile: {mobilePhoneNumber}", font=mainFont, fill=(mainColor)) # Mobile phone number
            businessCardImage.text((82,105), f"{username}@odoo.com", font=mainFont, fill=(mainColor)) # Email
        else:
            businessCardImage.text((82,93), f"{username}@odoo.com", font=mainFont, fill=(mainColor)) # Email

        businessCardImage.text((82,151), workAddressLine1, font=mainFont, fill=(mainColor)) # Address line 1
        businessCardImage.text((82,163), workAddressLine2, font=mainFont, fill=(mainColor)) # Address line 2
        businessCardImage.text((82,175), odooWebsite, font=mainFont, fill=(mainColor)) # Odoo website

        if not os.path.exists(f"{sys.argv[2]}/auto_generated_business-cards"):
            os.makedirs(f"{sys.argv[2]}/auto_generated_business-cards")
            
        img.save(f"{sys.argv[2]}/auto_generated_business-cards/{username}_businessCard_verso.png")
