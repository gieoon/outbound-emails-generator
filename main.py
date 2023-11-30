"""
Get list of company details including url's.
Generate an email for each of these companies.
Send them out to each of them.
"""

import asyncio
from scrape_website import get_company_website_details
from generate_outbound_email import generate_email

asyncio.get_event_loop().run_until_complete(main())

f = open('./companies_details.txt', 'r')
delimiter = '¿'

my_details = f"""
"""

async def main() -> None:
    for line in f.readlines():
        [company_name, company_url,company_phone,company_description,company_owner] = line.split('¿')

        [title, meta_description] = await get_company_website_details(company_url)
        email = await generate_email(title, meta_description, my_details)
        print('generated email: ', email)

        email_f = open('/generated_emails/' + company_name + '.txt', 'w')
        email_f.write(email)
        email_f.close()
        print('finished writing email for ', company_name)

asyncio.run(main())