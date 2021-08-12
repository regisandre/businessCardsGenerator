# Business cards

## Usage

```sh
./businessCardsGenerator.py --file "/home/odoo/Desktop/business-cards_test.csv" -o "/home/odoo/Desktop/"
./businessCardsGenerator.py -o "/home/odoo/Desktop/" --fullname "John Doe" --username "jodo" --jobTitle "Job Title" --phoneNumberExtension "4242" --mobilePhoneNumber "+32 496 XX XX XX" --location "LLN/ANT/GR1/GR2/GR3"
```
## Future updates
- Update the office location system by using a column in the CSV file or a parameter in the inline command
- Update the phone numbers management to hide both type of phone number if it doesn't exist
