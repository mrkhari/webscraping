import requests
from bs4 import BeautifulSoup
import mysql.connector

# Function to insert data into the MySQL database
def insert_into_database(data):
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="new_webscrabing"
    )

   

    cursor = connection.cursor()
    # Define the column names in the correct order
    columns = [
        "Name", "Position", "Telephone", "Email", "Website", "Address", "Postcode",
        "Area_served", "Notes", "Additional_Website", "Parking_available", "Time_of_day",
        "Session_Information", "Age_Groups", "Related_links", "cost_Details", "Accessibility",
        "Social_Media", "Parking_details", "Accreditation_details", "Venue_Email",
        "Venue_Website", "Transport"
    ]
    # Create a list of values in the correct order
    print(data.get('Parking_available', None))
    values = [data.get(column, None) for column in columns]

    # Insert the data into the database
    insert_query = f"INSERT INTO finaldata ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
    cursor.execute(insert_query, values)

    connection.commit()
    connection.close()

# Function to scrape details from a specific service page URL
def scrape_service_details(service_url):
    response = requests.get(service_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find('section', class_='field_section')
        dl_elements = element.find_all('dl')

        data = {}  # Create a dictionary to store scraped data

        # Extract and print the values from each dt and dd element within dl
        for dl in dl_elements:
            dt_elements = dl.find_all('dt')
            dd_elements = dl.find_all('dd')
            for dt, dd in zip(dt_elements, dd_elements):
                key = dt.text.strip()
                key = key.replace(' ','_')
                value = dd.text.strip()
                data[key] = value  # Store the data in the dictionary
                print(f"{key}: {value}")

        # Insert the data into the MySQL database
        insert_into_database(data)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# List of service URLs to scrape
service_urls = [
    "https://infolink.suffolk.gov.uk/kb5/suffolk/infolink/service.page?id=_OIcUh8eKWE"
    # Add more service URLs here
]

# Scrape details from each service page
for service_url in service_urls:
    print(f"Scraping details from: {service_url}")
    scrape_service_details(service_url)

# Loop through search result pages and scrape details
for i in range(1,500):
    url = f"https://infolink.suffolk.gov.uk/kb5/suffolk/infolink/results.page?qt=&term=London%2C+Little%2C+Suffolk&sorttype=distance&page={i}"
    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        Page = soup.find_all("a", class_="flex-grow-1")
        for np in Page:
            np_href = np.get("href")
            service_url = f"https://infolink.suffolk.gov.uk/kb5/suffolk/infolink/{np_href}"
            print(f"Scraping details from: {service_url}")
            scrape_service_details(service_url)
    else:
        print(f"Failed to retrieve search result page {i}. Status code: {r.status_code}")

   

            
            
