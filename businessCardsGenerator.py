#!/usr/bin/env python3

# https://code-maven.com/create-images-with-python-pil-pillow
import sys, re
from PIL import Image, ImageDraw, ImageFont

name = sys.argv[1]
username = sys.argv[2]
jobTitle = sys.argv[3]
phoneNumberExtension = ' '.join(re.findall('..',sys.argv[4])) # https://stackoverflow.com/questions/9475241/split-string-every-nth-character & https://www.geeksforgeeks.org/python-convert-list-of-strings-to-space-separated-string/
phoneNumber = f"+32 2  616 {phoneNumberExtension}"
mobilePhoneNumber = sys.argv[5]
workAddressLine1 = "Rue Laid Burniat, 5" # Multiline text : https://www.geeksforgeeks.org/python-pil-imagedraw-draw-multiline_text/
workAddressLine2 = "1348,  Louvain-la-Neuve"
odooWebsite = "www.odoo.com"

img = Image.new('RGB', (266, 175), color = (255, 255, 255)) # Image.open(r"pathToImageFile.png")
odooLogo = Image.open('resources/images/odooLogo.png', 'r');
odooLogo = odooLogo.resize((28, 9), Image.ANTIALIAS)


fnt="resources/fonts/arial.ttf"
mainFont = ImageFont.truetype(fnt, 7)
nameFont = ImageFont.truetype(fnt, 12)
jobTitleFont = ImageFont.truetype(fnt, 9)

mainColor = 0, 0, 0
jobTitleColor = 135, 91, 124

businessCardImage = ImageDraw.Draw(img)

img.paste(odooLogo, (20,29), odooLogo) # https://stackoverflow.com/questions/2563822/how-do-you-composite-an-image-onto-another-image-with-pil-in-python
businessCardImage.text((65,26), name, font=nameFont, fill=(mainColor)) # Name
businessCardImage.text((65,42), jobTitle, font=jobTitleFont, fill=(jobTitleColor)) # Job title
businessCardImage.line([(65,58), (246,58)], fill=jobTitleColor, width = 1) # https://www.geeksforgeeks.org/python-pil-imagedraw-draw-line/

businessCardImage.text((66,64), f"Tel: {phoneNumber}", font=mainFont, fill=(mainColor)) # Phone number
businessCardImage.text((66,73), f"Mobile: {mobilePhoneNumber}", font=mainFont, fill=(mainColor)) # Mobile phone number
businessCardImage.text((66,84), f"{username}@odoo.com", font=mainFont, fill=(mainColor)) # Email

businessCardImage.text((66,121), workAddressLine1, font=mainFont, fill=(mainColor)) # Address line 1
businessCardImage.text((66,130), workAddressLine2, font=mainFont, fill=(mainColor)) # Address line 2
businessCardImage.text((66,140), odooWebsite, font=mainFont, fill=(mainColor)) # Odoo website

img.save(f"{username}_businessCard_verso.png")
