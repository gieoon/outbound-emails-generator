# Given a URL, discovers the sitemap, or just the homepage and returns the text content to store.
import requests
import asyncio
from pyppeteer import launch

# Watch the directory you're running it from.
# f = open('./company_urls.txt', 'r')

async def get_company_website_details(url):

    browser = await launch(headless=True)
    page = await browser.newPage()

    # for company_url in f.readlines():
    #     print("company_url: ", company_url)
    await page.goto(company_url)

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
    meta_description = await page.evaluate('(element) => element.content', meta_description)
    print('meta_description:', meta_description)
    # content = await page.evaluate('document.body.textContent', force_expr=True)

    await browser.close()
    # f.close()

    return [title, meta_description]


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

# get_url_content("https://www.webbi.co.nz")