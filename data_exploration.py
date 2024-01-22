import requests
import pandas as pd
from bs4 import BeautifulSoup
# import fitz  # PyMuPDF
import PyPDF2
import re



# 1. Get Data from API as CSV files
# request sent to url
url = "https://data.cdc.gov/resource/3nzu-udr9.json"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # JSON response to a string
    json_str = response.text
    # string to a DataFrame
    data = pd.read_json(json_str)
    # display a few records
    print("A few records of the dataset:")
    print(data.head())
    # explore the size and dimensions of the dataset
    print("\nSize and Dimensions of the dataset:")
    print(f"Rows: {data.shape[0]}")
    print(f"Columns: {data.shape[1]}")
    print(f"Number of elements: {data.size}")

    # Identify missing data
    print("\nMissing data in each column?")
    print(data.isnull().sum())

    # Write the DataFrame to a CSV file
    data.to_csv('obesity_among_20.csv', index=False)
    print("Data downloaded and saved.")
else:
    print(f"Failed to download with the tatus code: {response.status_code}")







# 2. Web Scraping from HTML data 
# get response from url
url_web = 'https://www.cdc.gov/obesity/data/childhood.html'
response_web = requests.get(url_web)


if response_web.status_code == 200:
    # parse the HTML content
    soup = BeautifulSoup(response_web.content, 'html.parser')
    
    # find the relevant content
    obesity_data = soup.find_all('li', string=re.compile('Obesity prevalence was'))
   
    # lists to hold the extracted data
    age_groups = []
    prevalences_age = []
    ethnicities = []
    prevalences_ethnicity = []

    # extract data
    # obesity & age
    age_data = obesity_data[0].get_text()
    age_parts = age_data.split(',')
    for part in age_parts:
        match = re.search(r'(\d+.\d+)% among (.+)', part)
        if match:
            prevalences_age.append(float(match.group(1)))
            age_groups.append(match.group(2).strip())
    
    # obesity & age & race
    ethnicity_data = obesity_data[1].get_text()
    ethnicity_parts = ethnicity_data.split(',')
    for part in ethnicity_parts:
        match = re.search(r'(\d+.\d+)% among (.+)', part)
        if match:
            prevalences_ethnicity.append(float(match.group(1)))
            ethnicities.append(match.group(2).strip())

    # extracted data to DataFrames
    df_age_group = pd.DataFrame({'Age Group': age_groups, 'Obesity Prevalence (%)': prevalences_age})
    df_ethnicity = pd.DataFrame({'Ethnicity': ethnicities, 'Obesity Prevalence (%)': prevalences_ethnicity})

    # data to CSV files
    df_age_group.to_csv('obesity_age.csv', index=False)
    df_ethnicity.to_csv('obesity_ethnicity_age.csv', index=False)
else:
    print("Failed to retrieve.")
    







# 3. Data from PDF
file_path = '2023-ObesityReport-FINAL.pdf'
page_number = 28  # for the 28th page

with open(file_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    # extract text from the specific page
    page = pdf_reader.pages[page_number - 1]
    text = page.extract_text()

    # define the output filename for the extracted text
    output_filename = 'pdf_extracted_data.txt'

    # extracted text to .txt
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(text)
    