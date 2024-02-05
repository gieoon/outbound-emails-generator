import requests
import asyncio

UNSPLASH_APP_ID = 563419
UNSPLASH_ACCESS_KEY = "G4R0U2JuBeuAt6psW14EhzvgPQN8XDIVdnWN4TzCoxI"
UNSPLASH_SECRET_KEY = "g08H3UTNDF3qYVUYoX-RjVcwcy8IITT9YIXYaiqRJzE"
UNSPLASH_ENDPOINT = "https://api.unsplash.com/"

async def get_unsplash_images( business_type ):

    headers = {
        "Authorization": "Client-ID " + UNSPLASH_ACCESS_KEY,
        "Content-Type": "application/json",
    }

    # If you have query parameters, you can add them to the URL or use the 'params' parameter
    # For example, adding "?param1=value1&param2=value2" to the URL
    # Or using the 'params' parameter: params = {"param1": "value1", "param2": "value2"}

    response = requests.get(UNSPLASH_ENDPOINT + '/search/photos?query=' + business_type, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Successful request
        print("Response:", response.json())
        
        response = response.json()

        img_urls = []

        print(response)
        # response['results'])

        results_count = len( response['results'] ) 
        for result in response['results']:
            url = result['urls']['regular'] #'small' #'regular'
            img_urls.append( url )

        print("img_urls: ", img_urls)
        return img_urls

    else:
        # Handle the error
        print(f"Error: {response.status_code}, {response.text}")
        return ['', '', '']

asyncio.run( get_unsplash_images("amazon delivery services") )