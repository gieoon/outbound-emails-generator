# Given a URL, discovers the sitemap, or just the homepage and returns the text content to store.
import requests
import asyncio
import re 
from _openai import extract_from_page
# Watch the directory you're running it from.
# f = open('./company_urls.txt', 'r')

async def get_company_website_details(page, url):
    
    # return type [title, meta_description, emails, owners]
    return await get_url_details(page, url, "")

async def get_url_details(page, company_url, content, no_recursion=False):
    # for company_url in f.readlines():
    #     print("company_url: ", company_url)
    try:
        await page.goto(company_url)
    except:
        return [None, None, None, None, None]
    # dimensions = await page.evaluate('''() => {
    # return {
    #     width: document.documentElement.clientWidth,
    #     height: document.documentElement.clientHeight,
    #     deviceScaleFactor: window.devicePixelRatio,
    #     }
    # }''')

    # print(dimensions)
    
    # page_content = await page.evaluate("() => document.body.innerText.replaceAll('\n', ' ')")
    # page_content = await page.evaluate('document.body.innerText', force_expr=True) 
    # page_content = page_content.replace('\\n', ' ')
    # print('page_content:', page_content)

    # await page.$eval("head > meta[name='description']", element => element.content);
    title = await page.title()
    print('title:', title)
    meta_description = await page.querySelector("head > meta[name='description']")
    if meta_description:
        meta_description = await page.evaluate('(element) => element.content', meta_description)
    else:
        meta_description = ''

    print('meta_description:', meta_description)
    content += await page.evaluate('document.body.innerText', force_expr=True)
    content = content.replace('\n', ' ')

    # Get email
    emails = get_email(content)
    [owners, company_name] = await extract_from_page(content)
    # phone_numbers = get_phone_number(content)
    # Check /about and /contact
    if no_recursion == False:
        if len(emails) == 0:# or len(phone_numbers) == 0:
            print('Going to /contact page')
            [_, _, emails, owners, company_name] = await get_url_details(page, company_url + '/contact', content, no_recursion=True)
            
            # if len(emails) == 0 or len(phone_numbers) == 0:
            #     [_, _, emails, phone_numbers] = await get_url_details(page, company_url + '/about', no_recursion=True)

    return [title, meta_description, emails, owners, company_name]

def get_email(content):

    z = re.findall(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])", content)
    print('z:', z)
    if len(z):

        print('emails found: ', z)
        emails = z
        return emails
    return []


# def get_phone_number(content):
#     print('content', content)
#     z = re.match(r"(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}", content)
#     if len(z):
#         print('phone numbers found: ', z)
#         phone_numbers = z
        
#         return phone_numbers
#     return []
    
# import requests
# from bs4 import BeautifulSoup

# def get_url_content(url):

#     response = requests.get(url)
#     html_page = response.content
#     soup = BeautifulSoup(html_page, 'html.parser')
    
#     # print(soup.prettify())
#     text = soup.find_all(string=True)

#     text_output = ""
#     blacklist = [
#         '[document]',
#         'noscript',
#         'header',
#         'html',
#         'meta',
#         'head', 
#         'input',
#         'script',
#         'style',
#     ]

#     for t in text:
#         if t.parent.name not in blacklist or True:
#             text_output += f"{t} "

#     print(text_output)

# import asyncio
# asyncio.run(get_company_website_details("https://www.webbi.co.nz"))
