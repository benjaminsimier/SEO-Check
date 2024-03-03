from flask import Flask, render_template, request, send_file
from SeoTest import test_seo, fetch_sitemap, extract_urls_from_sitemap
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sitemap_url = request.form['sitemap_url']
        sitemap_content = fetch_sitemap(sitemap_url)
        if sitemap_content:
            urls = extract_urls_from_sitemap(sitemap_content)
            output_folder = "reports"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            output_file = os.path.join(output_folder, "seo_results.csv")
            test_seo(urls, output_file)  # Pass both urls and output_file
            if os.path.exists(output_file):
                return send_file(output_file, as_attachment=True)
            else:
                return "Failed to perform SEO tests or generate CSV file."
        else:
            return "Failed to fetch sitemap."
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
