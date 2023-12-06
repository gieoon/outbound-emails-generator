import asyncio
import os 
import re 
from emailer import send_plain_data

directory_path = './generated_emails/'

async def send_emails():
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        file_list = os.listdir(directory_path)
        print("file_list: ", file_list)
        
        for filename in file_list:
            
            # TODO remove this.
            if 'Webbi Digital Studio.txt' != filename:
                continue

            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path):
                print(f"Processing file: {filename}")

                f = open(file_path, 'r', encoding='utf-8')
                content = f.read()
                [destination_email, company_name, subject, owners, email_stripped] = extract_shit(content)

                if len(owners) == 0:
                    owners = company_name
                
                email_stripped = email_stripped.replace('\n', '<br/>')

                print("====== PREPARING TO SEND EMAIL ======")
                print('Address:', destination_email)
                print('subject:', subject)
                print('owners:', owners)
                print('====== Email content ======\n', email_stripped, '\n====== END OF EMAIL CONTENT ======\n')
                val = input('Press Enter to approve and send . . .')
                if len(val) == 0:
                    send_plain_data(destination_email, company_name, subject, email_stripped, owners , retry_count=0)
                else:
                    input('Not sending and skipping to the next email')
    else:
        print(f"The directory '{directory_path}' does not exist.")



def extract_shit(email_file):
    # print('email_file', email_file)
    pattern = r'Subject:[ ]*(.*)'
    match = re.search(pattern, email_file)
    # print('match[0]', match[0])
    
    if match:
        subject_text = match.group(1).strip()
        # print('subject_text', subject_text)
        email_stripped = email_file.replace(match[0], '')
        # print('Subject=>', subject_text)
    else:
        print('Subject not found')

    pattern3 = r'Email:[ ]*(.*)'
    match3 = re.search(pattern3, email_stripped)
    # print('match3[0]', match3[0])
    if match3:
        destination_email = match3.group(1).strip()
        # print('destination_email', destination_email)
        email_stripped = email_stripped.replace(match3[0], '')
    else:
        print("destination email not found")


    # print("email_stripped 1: ", email_stripped)
    pattern2 = r'Owners:[ ]*(.*)'
    match2 = re.search(pattern2, email_stripped)
    if match2:
        owners_text = match2.group(1).strip()
        # print('owners_text', owners_text)
        # print('match2[0]', match2[0], 'end')
        email_stripped = email_stripped.replace(match2[0], '')
    else:
        print("Owners not found")
    # print("email_stripped 2: ", email_stripped)

    pattern4 = r'Company Name:[ ]*(.*)'
    match4 = re.search(pattern4, email_stripped)
    # print('match4[0]', match4[0])
    if match4:
        company_name = match4.group(1).strip()
        # print("company_name", company_name)
        email_stripped = email_stripped.replace(match4[0], '')
    else:
        print("company name not found")
    return [destination_email, company_name, subject_text, owners_text, email_stripped.replace('Content:', '').strip()]


# content = """
# Subject: Elevate Your Online Presence with Expert Design & SEO

# Content:

# Hi there,

# Hope you're having a fantastic day! I'm Jun, the face behind Webbi Digital Studio here in beautiful New Zealand. Our team specializes in crafting websites that are not just stunning, but also highly effective in turning visitors into customers.
# """
# [subject, stripped] = extract_subject(content)
# print('stripped:', stripped)
asyncio.run(send_emails())