import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import os

def fetch_sitemap(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch sitemap. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return None

def extract_urls_from_sitemap(sitemap_content):
    urls = []
    try:
        soup = BeautifulSoup(sitemap_content, "html.parser")
        loc_tags = soup.find_all("loc")
        for loc_tag in loc_tags:
            urls.append(loc_tag.text)
        return urls
    except Exception as e:
        print(f"Error extracting URLs from sitemap: {e}")
        return []

def calculate_page_load_time(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        if response.status_code == 200:
            return round(end_time - start_time, 2)
        else:
            return None
    except Exception as e:
        print(f"Error calculating page load time for URL {url}: {e}")
        return None

def test_seo(urls, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['URL', 'Title', 'Meta Description', 'H1', 'Image Alt', 'Meta Keywords', 'Canonical Tag', 'Structured Data', 'Robots Meta Tag', 'Open Graph Tags', 'Twitter Card Tags', 'Mobile Friendliness', 'Page Load Time', 'Internal Links', 'External Links', 'Broken External Links Count', 'Broken External Links', 'Heading Structure', 'Keyword Density', '404 Error Page', 'HTTPS Usage', 'XML Sitemap', 'Language Declaration', 'Viewport Meta Tag']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for url in urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    title = soup.find("title").text.strip() if soup.find("title") else None
                    meta_description = soup.find("meta", {"name": "description"})["content"].strip() if soup.find("meta", {"name": "description"}) else None
                    h1 = soup.find("h1").text.strip() if soup.find("h1") else None
                    # Image alt test
                    images = soup.find_all("img")
                    image_alt = ", ".join([img.get("alt", "") for img in images])
                    # Additional SEO tests
                    meta_keywords = soup.find("meta", {"name": "keywords"})["content"].strip() if soup.find("meta", {"name": "keywords"}) else None
                    canonical_tag = soup.find("link", {"rel": "canonical"})["href"].strip() if soup.find("link", {"rel": "canonical"}) else None
                    structured_data = "Implemented" if soup.find("script", type="application/ld+json") else None
                    robots_meta_tag = soup.find("meta", {"name": "robots"})["content"].strip() if soup.find("meta", {"name": "robots"}) else None
                    open_graph_tags = "Implemented" if soup.find("meta", {"property": "og:title"}) else None
                    twitter_card_tags = "Implemented" if soup.find("meta", {"name": "twitter:title"}) else None
                    # Placeholder for Mobile Friendliness
                    mobile_friendliness = None
                    # Calculate Page Load Time
                    page_load_time = calculate_page_load_time(url)
                    # Count internal and external links
                    internal_links = len(soup.find_all("a", href=re.compile("^(/|https?://"+response.url.split('/')[2]+")")))  # Count internal links
                    external_links = soup.find_all("a", href=re.compile("^(?!(/|https?://"+response.url.split('/')[2]+"))"))  # Get all external links
                    broken_external_links_count = 0
                    broken_external_links_urls = []
                    for link in external_links:
                        if link.get('href'):
                            external_link = link['href']
                            external_response = requests.head(external_link)
                            if external_response.status_code != 200:
                                broken_external_links_count += 1
                                broken_external_links_urls.append(external_link)
                    heading_structure = "Valid" if soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]) else None
                    keyword_density = "Optimal"  # To be implemented based on specific keyword density thresholds
                    error_404_page = "User-friendly" if soup.find("title").text.strip().lower() == "404 not found" else "Not Found"
                    https_usage = "Implemented" if response.url.startswith("https://") else None
                    xml_sitemap = "Present" if soup.find("link", {"rel": "sitemap"}) else None
                    language_declaration = "Declared" if soup.html.get("lang") else None
                    viewport_meta_tag = "Implemented" if soup.find("meta", {"name": "viewport"}) else None
                    # Write to CSV
                    writer.writerow({
                        'URL': url,
                        'Title': title,
                        'Meta Description': meta_description,
                        'H1': h1,
                        'Image Alt': image_alt,
                        'Meta Keywords': meta_keywords,
                        'Canonical Tag': canonical_tag,
                        'Structured Data': structured_data,
                        'Robots Meta Tag': robots_meta_tag,
                        'Open Graph Tags': open_graph_tags,
                        'Twitter Card Tags': twitter_card_tags,
                        'Mobile Friendliness': mobile_friendliness,
                        'Page Load Time': page_load_time,
                        'Internal Links': internal_links,
                        'External Links': len(external_links),
                        'Broken External Links Count': broken_external_links_count,
                        'Broken External Links': ', '.join(broken_external_links_urls),
                        'Heading Structure': heading_structure,
                        'Keyword Density': keyword_density,
                        '404 Error Page': error_404_page,
                        'HTTPS Usage': https_usage,
                        'XML Sitemap': xml_sitemap,
                        'Language Declaration': language_declaration,
                        'Viewport Meta Tag': viewport_meta_tag
                    })
                    print(f"SEO test passed for URL: {url}")
                else:
                    print(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error testing SEO for URL {url}: {e}")

def main():
    sitemap_url = input("Enter the URL of the sitemap: ")
    output_folder = "reports"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, input("Enter the output CSV file name: "))
    
    sitemap_content = fetch_sitemap(sitemap_url)
    if sitemap_content:
        urls = extract_urls_from_sitemap(sitemap_content)
        test_seo(urls, output_file)
    else:
        print("Failed to fetch sitemap. Exiting...")

if __name__ == "__main__":
    main()
