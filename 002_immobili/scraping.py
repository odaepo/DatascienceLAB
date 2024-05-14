import requests
import re
import pandas as pd
import unicodedata
import time
from io import BytesIO
from bs4 import BeautifulSoup
from collections import namedtuple

# Function to scrape the houses
def find_houses():    

    # Load the cities dataset
    df_cities=pd.read_csv('Dataset/cities.csv', low_memory=False)
    
    # Get a sample of 1000 cities
    df_cities = df_cities.sample(n=2)

    all_results = []
    a = 1
    total = len(df_cities)

    # Loop through the cities
    for i, row in df_cities.iterrows():
        urls = []

        try:
            # Get the city, province, region, and distribution
            city = row['comune'].replace(' ', '-').replace("'", "-").lower()
            city = unicodedata.normalize('NFKD', city).encode('ASCII', 'ignore').decode('utf-8')

            province = row['provincia']
            region = row['regione']
            distribution = row['ripartizione_geografica']
    
            # Print the current city
            print(f'{city} - {a} of {total} cities')
            
            # Get the for the houses's urls in the city
            urls = get_urls(city)

            b = 1
            total1 = len(urls)

            # Loop through the houses's urls
            for url in urls:
                # Print the current house
                print(f'{city} - Get house {b} of {total1} - {url}')
                
                # Get the house's data
                try:                    
                    all_results.append(get_data(url, city, province, region, distribution))
                except:
                    print(f"Error url '{url}'")
                    raise
                b += 1
            a += 1

        except:
            print(f"Error city='{city}'")
            raise

    # Get a dataframe from the results    
    df = pd.DataFrame(all_results)
    print("End of scraping")
    return df

# Function to get the urls of the houses
def get_urls(city, get_all_pages=False):
    
    # Regular expression to match the urls
    pattern = re.compile(r'\d+\/$')
    urls = []

    # Url of the city first page
    url = f'https://www.immobiliare.it/vendita-case/{city}/?criterio=rilevanza'
            
    # Get first page
    print(f'{city} - Get page 1')
    page = get_page(url)
    page.seek(0)

    # Parse the page
    soup = BeautifulSoup(page, 'html.parser')

    # For all urls in first page
    for link in soup.find_all('a'):
        l = link.get('href')
        
        # If the url is None skip it
        if l is None:
            continue
        
        # If the url is a house url add it to the list
        if 'https' in l and 'annunci' in l:
            if pattern.search(l):
                urls.append(l)
        
    # Get other pages
    if get_all_pages:

        # For all pages. 1000 is an arbitrary number
        for i in range(2, 1000):
            # Print the current page
            print(f'{city} - Get page {i}')

            # Get the current page
            curr_url = url + f'&pag={i}'
            t = get_text(curr_url).lower()

            # Check if the page is empty
            if '404 not found' in t or 'non è presente' in t:
                break
            else:
                # Get the page
                page = get_page(curr_url)
                page.seek(0)

                # Parse the page
                soup = BeautifulSoup(page, 'html.parser')

                # For all urls in the page
                for link in soup.find_all('a'):
                    l = link.get('href')

                    # If the url is None skip it
                    if l is None:
                        continue
                    
                    # If the url is a house url add it to the list
                    if 'https' in l and 'annunci' in l:
                        if pattern.search(l):
                            urls.append(l)

    # Print the number of houses found and return the list of urls
    print(f'Found {len(urls)} houses found.')
    return urls

# Function to get the page
def get_page(url):    
    req = requests.get(url, allow_redirects=False)
    page = BytesIO()
    page.write(req.content)    
    return page

# Function to get the text of the page
def get_text(url):

    # Get the page
    page = get_page(url)

    # Parse the page
    soup = BeautifulSoup(page, 'html.parser')  

    # Get the text  
    text = soup.get_text() 
    
    # Cleaning text
    t = text.replace('\n', '')
    for _ in range(50):
        t = t.replace('  ', ' ')

    return t

# Function to get the data of the house
def get_data(url, city, province, region, distribution):

    # Get the house page
    page = get_page(url)
    page.seek(0)

    # Parse the house page
    soup = BeautifulSoup(page, 'html.parser')

    # Find div with the price and get the value
    price = ''
    div = soup.find(attrs={'class': 'in-detail__mainFeaturesPrice'})
    if div is not None:
        price = div.getText()
    else:
        div = soup.find(attrs={'class': 'in-prices'})
        price =  div.getText() if div is not None else ''

    # Find div with the rooms and get the value
    div = soup.find(attrs={'aria-label': 'locali'})
    rooms = div.getText() if div is not None else ''

    # Find div with the surface and get the value
    div = soup.find(attrs={'aria-label': 'superficie'})
    surface = div.getText() if div is not None else ''

    # Find div with the bathrooms and get the value
    bathrooms = ''
    div = soup.find(attrs={'aria-label': 'bagni'})
    if div is not None:
        bathrooms = div.getText()
    else:
        div = soup.find(attrs={'aria-label': 'bagno'})
        bathrooms = div.getText() if div is not None else ''

    # Find div with the floor and get the value
    #div = soup.find(attrs={'aria-label': 'piano'})
    #floor = div.getText() if div is not None else ''

    # Find div with the energy_class and get the value
    div = soup.find(attrs={'class': 'in-realEstateFeatures__energy'})
    energy_class = div.getText() if div is not None else ''

    # Find div with the city and address and get the value
    #city = ''
    address = ''
    href_title = soup.find_all('a', {'class': 're-title__link'})
    for tag in href_title:
        span_location = tag.find_all('span', {'class': 're-title__location'})
        i = 0
        for tag1 in span_location:
            if i == 0:
                #city = tag1.getText()
                pass
            else:
                address = tag1.getText()
            i += 1
    
    # Find div with the title and get the value
    div = soup.find(attrs={'class': 're-title__title'})
    title = div.getText() if div is not None else ''

    # Find div with the description and get the value
    div = soup.find(attrs={'class': 'in-readAll--lessContent'})
    description = div.getText() if div is not None else ''
    
    reference = ""
    contract = ""
    floor = ""
    total_floor = ""
    typology = ""
    year = ""
    heating = ""
    air_conditioning = ""
    
    # Find div with the features
    dt_title_feature = soup.find_all('dt', {'class': 'in-realEstateFeatures__title'})
    
    # Loop through the features
    for tag in dt_title_feature:
        title_feature = tag.getText()
    
        # Get 'riferimento e data annuncio'
        if title_feature.lower() == 'riferimento e data annuncio':
            dd_value_feature = tag.find_next('dd', {'class': 'in-realEstateFeatures__value'})
            reference = dd_value_feature.getText()
        
        # Get 'contratto'
        elif title_feature.lower() == 'contratto':
            dd_value_feature = tag.find_next('dd', {'class': 'in-realEstateFeatures__value'})
            contract = dd_value_feature.getText()
 
        # Get 'piano'
        elif title_feature.lower() == 'piano':
            dd_value_feature = tag.find_next('dd', {'class': 'in-realEstateFeatures__value'})
            floor = dd_value_feature.getText()

        # Get 'totale piani edificio'
        elif title_feature.lower() == 'totale piani edificio':
            dd_value_feature = tag.find_next('dd', {'class': 'in-realEstateFeatures__value'})
            total_floor = dd_value_feature.getText()        
        
        # Get 'tipologia'
        elif title_feature.lower() == 'tipologia':
            dd_value_feature = tag.find_next('dd', {'class': 'in-realEstateFeatures__value'})
            typology = dd_value_feature.getText()

        # Get 'anno di costruzione'
        elif title_feature.lower() == 'anno di costruzione':
            dd_value_feature = tag.find_next('dd', {'class': 'in-realEstateFeatures__value'})
            year = dd_value_feature.getText()
        
        # Get 'riscaldamento'
        elif title_feature.lower() == 'riscaldamento':
            dd_value_feature = tag.find_next('dd', {'class': 'in-realEstateFeatures__value'})
            heating = dd_value_feature.getText()

        # Get 'climatizzatore'
        elif title_feature.lower() == 'climatizzatore':
            dd_value_feature = tag.find_next('dd', {'class': 'in-realEstateFeatures__value'})
            air_conditioning = dd_value_feature.getText()

    # Find tag with the other characteristics
    other_characteristics = ""
    dd = soup.find_all('dd', {'class': 'in-realEstateFeatures__badgeContainer'})

    # Loop through the other characteristics
    for tag in dd:

        # Get the div with the other characteristics
        div_feature = tag.find_all('div', {'class': 'in-realEstateFeatures__badge'})

        # Loop through the other characteristics
        for div in div_feature:
            other_characteristics += div.getText() + ' | '

    # Create a namedtuple with the house data
    House = namedtuple(
        'House', [
            'prezzo',
            'stanze',
            'superfice',
            'bagni',
            'piano',
            'totale_piani',
            'citta',
            'provincia',
            'regione',
            'ripartizione_geografica',
            'indirizzo',
            'tipologia',
            'anno_costruzione',
            'riscaldamento',
            'climatizzatore',
            'classe_energetica',
            'altre_caratteristiche',
            'titolo',
            'descrizione',
            'riferimento',
            'contratto',
            'url'
        ]
    )
    
    # Create the house object
    res = House(
        price,
        rooms,
        surface,
        bathrooms,   
        floor,
        total_floor,
        city,
        province,
        region,
        distribution, 
        address,
        typology,
        year,
        heating,
        air_conditioning,
        energy_class,
        other_characteristics,
        title,
        description,
        reference,
        contract,
        url
    )

    # Return the house object
    return res

# Start the scraping
start = time.time()

# Scrape the houses
df = find_houses()

# Save the raw dataset
df.to_csv('Dataset/sale_raw.csv', index=True)

# End the scraping
end = time.time()

# Print the execution time
print(f'Execution time: {end - start} seconds')
