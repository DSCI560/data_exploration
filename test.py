import requests
from bs4 import BeautifulSoup
import textract

# Function to download PDF from a given URL
def download_pdf(url, output_path):
    response = requests.get(url)
    with open(output_path, 'wb') as file:
        file.write(response.content)

# Function to extract text from PDF document
def extract_pdf_text(file_path):
    text = textract.process(file_path, method='pdftotext')
    return text.decode('utf-8')

# Function to scrape text from an HTML page
def scrape_html_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    # Get text
    text = soup.get_text()
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

# URLs of the PDFs to be downloaded
pdf_urls = [
    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9863459/pdf',
    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6959843/pdf'
]

# Local paths to save the downloaded PDFs
pdf_paths = [
    'sugars_intake_2010_2015.pdf',
    'sugar_obesity_review.pdf'
]

# Download and extract text from PDFs
for url, path in zip(pdf_urls, pdf_paths):
    print(f"Downloading PDF from {url} to {path}...")
    download_pdf(url, path)
    print(f"Extracting text from {path}...")
    text = extract_pdf_text(path)
    print(f"Text extracted from {path}:\n{text[:1000]}")  # Printing first 1000 characters of the text

# NCBI article URL for HTML scraping
html_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9863459/'
print("\nScraping HTML page...")
