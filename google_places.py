import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_PLACES_API_KEY'))

filename = './companies_place_data2.txt'
f2 = open(filename, 'w', encoding='utf-8')
f2.write("")
f2.close()

def searchNearby(query):
    url = 'https://places.googleapis.com/v1/places:searchText'

    api_key = os.environ.get('GOOGLE_PLACES_API_KEY')

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': '*', #'places.displayName,places.formattedAddress,places.priceLevel'
    }

    data = {
        'textQuery': query,
        # 'maxResultsCount': 30,
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    # print('response: ', response)
    # Print the response
    response_json = json.loads(response.text)
    # print(response_json['places'][0])

    print('Number of places: ', len(response_json['places']))
    n = 0
    for place in response_json['places']:
        n += 1

        # Only get low rating services.
        # if place['userRatingCount'] < 10:
        #     print('maps uri: ', place['googleMapsUri'])

        # TODO remove this
        # if n < 2:
        place_obj = process_place(place)

no_website_count = 0

def process_place (place):
    out = {}
    global no_website_count


    # Number of ratings
    out['url'] = 'https://www.google.com/maps/place/?q=place_id:' + place['id']
    out['national_phone_number'] = place['nationalPhoneNumber'] if 'nationalPhoneNumber' in place else 'no phone number'
    out['international_phone_number'] = place['internationalPhoneNumber'] if 'internationalPhoneNumber' in place else 'no phone number'
    out['formatted_address'] = place['formattedAddress']
    out['utc_offset_minutes'] = place['utcOffsetMinutes']
    if 'rating' in place:
        out['rating'] = place['rating']
    out['google_maps_uri'] = place['googleMapsUri']

    
    out['website_uri'] = place['websiteUri'] if 'websiteUri' in place else 'no website'
    if 'websiteUri' not in place:
        no_website_count += 1
    
    out['adr_format_address'] = place['adrFormatAddress']
    out['business_status'] = place['businessStatus']
    if 'userRatingCount' in place:
        out['user_rating_count'] = place['userRatingCount']       
    out['display_name'] = place['displayName']['text']
    out['language'] = place['displayName']['languageCode']
    out['short_formatted_address'] = place['shortFormattedAddress']
    out['reviews'] = []
    if 'reviews' in place:
        for review in place['reviews']:
            # print('review: ', review)
            out['reviews'].append({
                "rating": review['rating'],
                'text': review['text']['text'] if 'text' in review else '',
                'language': review['text']['languageCode'] if 'text' in review else '',
                'author': review['authorAttribution']['displayName'],
                'photo': review['authorAttribution']['photoUri'],
                'uri': review['authorAttribution']['uri'],
                'publish_time': review['publishTime']
            })
    # print(out)

    # Test only saving businesses with no websites.
    if 'websiteUri' in place:
        return
    
    
    # print('place: ', place)
    # input("\n...\n")

    def process_file_name(place_name):
        return place_name.replace('|', '').replace(r"[ ]{2,}", ' ')

    out_filename = process_file_name(out['display_name'])
    # print('Saving as ', out_filename)
    f = open('./places_data/' + out_filename + '.txt', 'w', encoding='utf-8')
    f3 = open('./places_data_truncated/' + out_filename + '.txt', 'w', encoding='utf-8')
    for key in out:
        if key == 'reviews':
            for review in out['reviews']:
                f.write('==== Review ====\n')
                for review_key in review:
                    # print("review_key", review_key, review)
                
                    f.write(f"{review_key}: {review[review_key]}\n")
                    if review_key == 'text':
                        f3.write(f"{review[review_key]}\n\n")
                
        else: 
            f.write(f"{key}:{out[key]}\n")
            if key == 'display_name' or key == 'formatted_address' or key == 'national_phone_number':
                f3.write(f"{out[key]}\n")
    f.close()
    f3.close()

    delimiter = '¿'

    # f2 = open('./companies_place_data.txt', 'a', encoding='utf-8')
    global filename
    f2 = open(filename, 'a', encoding='utf-8')

    # google_maps_url, company_name, company_url, company_phone, company_description, company_owners
    # print(out['url'])
    f2.write(out['url'].replace(r"\/", '') + delimiter)
    f2.write(out['display_name'] + delimiter)
    f2.write(out['website_uri'] + delimiter)
    f2.write(out['national_phone_number'] + delimiter)
    f2.write('' + delimiter)
    f2.write('')
    f2.write('\n')

    f2.close()
# searchNearby('Website developers in Nelson, New Zealand')
# query = "Webbi Digital Studio, Richmond Nelson"
# query = "Rotary Clubs in Auckland"
# query = "Construction companies in Christchurch"
query = "new zealand nelson stoke hairdresser"
searchNearby(query)

print('no websites: ', no_website_count, '/20')