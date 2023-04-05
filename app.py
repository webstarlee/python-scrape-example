from bs4 import BeautifulSoup
from selenium import webdriver
 
driver = webdriver.Chrome()

url = "https://www.realtor.com/realestateagents/5a8730962061c5001094f042/"

driver.get(url)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
about_section = soup.find("div", id="about-section")
profile_section = about_section.find('div', id='profile-section')
profile_detail = profile_section.find("div", class_="profile-details")
username = profile_detail.find("p", class_="profile-Tiltle-main").text
company_p_list = profile_detail.find_all("p", class_="profile-Tiltle-sub")
company_name = ''
if company_p_list != None:
    for company_p in company_p_list:
        if not "#" in company_p.text:
            company_name = company_p.text

contact_section = about_section.find("div", id="contact-details")
contact_detail_container = contact_section.find_all("a")
phone_numers_list = []
wensite_url_list = []
seocial_media_list = []
if contact_detail_container != None:
    for link in contact_detail_container:
        link_name = link.get('data-linkname')
        if "agent_details:contact_details:mobile" in link_name:
            phone_numers_list.append(link)
        elif "agent_details:contact_details:website" in link_name or "agent_details:about:brokerage_website" in link_name:
            wensite_url_list.append(link)
        elif "agent_details:about:social_media" in link_name:
            seocial_media_list.append(link)
        print(link_name)

phone_numbers = []
if len(phone_numers_list)>0:
    for item in phone_numers_list:
        number_span = item.find("span")
        type_span = item.find_next_sibling('span')
        if number_span != None:
            number = number_span.text
            if type_span != None:
                number_type = type_span.text
                phone_numbers.append({"number": number, "type": number_type})
            else:
                phone_numbers.append({"number": number})

websites = []
if len(wensite_url_list)>0:
    for item in wensite_url_list:
        website_title = item.text
        website_url = item.get('href')
        type_span = item.find_next_sibling('span')
        if type_span != None:
            url_type = type_span.text
            websites.append({"title": website_title, "url": website_url, "type": url_type})
        else:
            websites.append({"title": website_title, "url": website_url})

social_medias = []
if len(seocial_media_list)>0:
    for item in seocial_media_list:
        social_title = item.text
        social_url = item.get('href')
        social_medias.append({"title": social_title, "url": social_url})


address_detail_container = contact_section.find("div", class_="better-homes-and-gar")
address_detail_div = address_detail_container.find("div", class_="better-homes-and-gar-icon-right")
address_title_p= address_detail_div.find("p", class_="addressspace")
address_location_p = address_detail_div.find("p", class_="agent_address")

address_title = ''
if address_title_p != None:
    address_title = address_title_p.text

address_location = ''
if address_location_p != None:
    address_location_spans = address_location_p.find_all('span')
    if address_location_spans != None:
        for item in address_location_spans:
            if address_location != "":
                address_location += ", "
            address_location += item.text


file_name = username.strip()+".txt"
f = open("data/"+file_name, "w")
f.write('Username: ' + str(username).strip())
f.write('\nCompany Name: ' + str(company_name).strip())
if len(phone_numbers)>0:
    for phone_number in phone_numbers:
        f.write('\n'+phone_number['type'].strip()+' Number: ' + str(phone_number['number'].strip()))

if len(websites)>0:
    for website in websites:
        f.write('\n'+website['title'].strip()+" "+website['type'].strip()+': ' + str(website['url'].strip()))

if len(social_medias)>0:
    for social_media in social_medias:
        f.write('\n'+social_media['title'].strip()+': ' + str(social_media['url']).strip())

f.write('\n'+address_title+' address: ' + str(address_location))

f.close()