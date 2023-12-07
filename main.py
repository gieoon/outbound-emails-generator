"""
Get list of company details including url's.
Generate an email for each of these companies.
Send them out to each of them.
"""

import asyncio
from pyppeteer import launch
from scrape_website import get_company_website_details
from _openai import generate_email

# This file is populated from google_places.py
f = open('./companies_place_data.txt', 'r', encoding='utf-8')
delimiter = '¿'

# my_details = f"""
# My company name: Webbi Digital Studio 
# My company description: A New Zealand-based website design agency building conversion focused websites that grow your brand. Sample work can be found on our home page so you can get an idea of what to expect.
# """

my_details = f"""
My company name: Webbi 
My company description: A New Zealand-based website design team building fast, stunning and conversion focused websites that grow brands. Sample work is on our home page.
"""

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()

    index = 0
    for line in f.readlines():
        index += 1
        if index > 88:
            print('reading line:', index, line)
            [google_maps_url, google_maps_company_name, company_url, company_phone, company_description, company_owners] = line.split('¿')
            print('loaded: ', google_maps_url, google_maps_company_name, company_url, company_phone, company_description, company_owners)
            
            if company_url != 'no website':
                [title, meta_description, emails, owners, company_name] = await get_company_website_details(page, company_url)
            if company_url == 'no website' or title == None:
                title = google_maps_company_name
                meta_description = google_maps_company_name
                emails = []
                owners = []
                company_name = google_maps_company_name
            
            print("parent company_name", company_name)
            print("generating email . . . ")

            if len(company_name) == 0:
                print('replacing company name')
                company_name = google_maps_company_name
            
            email = await generate_email(title, meta_description, owners, company_name, my_details)
            print('generated email: ', email)
            # email = ''

            email = "Company Name: " + company_name + '\n' + email
            if isinstance(emails, str):
                emails = [emails]
            email = "Email: " + ','.join(emails) + '\n' + email
            if isinstance(owners, str):
                owners = [owners]
            email = "Owners: " + ','.join(owners) + '\n' + email

            email_f = open('./generated_emails/' + company_name + '.txt', 'w', encoding='utf-8')
            email_f.write(email)
            email_f.close()
            print('finished writing email for ', company_name)

    await browser.close()


asyncio.run(main())

# asyncio.get_event_loop().run_until_complete(main())