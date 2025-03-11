from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to get PageSpeed Insights
def get_page_speed_insights(url):
    api_key = '[YOUR_API_KEY]'
    endpoint = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}'
    
    try:
        response = requests.get(endpoint)
        data = response.json()

        # Check for errors in response
        if 'error' in data:
            return {'error': data['error']['message']}

        # CrUX Metrics (Chrome User Experience Report)
        crux_metrics = {
            "First Contentful Paint": data.get('loadingExperience', {}).get('metrics', {}).get('FIRST_CONTENTFUL_PAINT_MS', {}).get('category', 'N/A'),
            "First Input Delay": data.get('loadingExperience', {}).get('metrics', {}).get('FIRST_INPUT_DELAY_MS', {}).get('category', 'N/A')
        }

        # Lighthouse Metrics
        lighthouse_metrics = {
            'First Contentful Paint': data.get('lighthouseResult', {}).get('audits', {}).get('first-contentful-paint', {}).get('displayValue', 'N/A'),
            'Speed Index': data.get('lighthouseResult', {}).get('audits', {}).get('speed-index', {}).get('displayValue', 'N/A'),
            'Time To Interactive': data.get('lighthouseResult', {}).get('audits', {}).get('interactive', {}).get('displayValue', 'N/A'),
            'First Meaningful Paint': data.get('lighthouseResult', {}).get('audits', {}).get('first-meaningful-paint', {}).get('displayValue', 'N/A'),
            'First CPU Idle': data.get('lighthouseResult', {}).get('audits', {}).get('first-cpu-idle', {}).get('displayValue', 'N/A'),
            'Estimated Input Latency': data.get('lighthouseResult', {}).get('audits', {}).get('estimated-input-latency', {}).get('displayValue', 'N/A')
        }

        return {
            'crux_metrics': crux_metrics,
            'lighthouse_metrics': lighthouse_metrics
        }

    except Exception as e:
        return {'error': f'Failed to retrieve PageSpeed Insights: {str(e)}'}

# Route to handle SEO analysis
@app.route('/analyze', methods=['POST'])
def analyze_seo():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            return jsonify({'error': f'Failed to fetch URL, status code: {response.status_code}'}), 400

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else 'No title'
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_description['content'] if meta_description else 'No meta description'
        h1_tags = [h1.text for h1 in soup.find_all('h1')]
        image_alt_texts = [img.get('alt', 'No alt text') for img in soup.find_all('img')]

        # Get PageSpeed Insights Data
        page_speed_data = get_page_speed_insights(url)

        seo_data = {
            'title': title,
            'meta_description': meta_description,
            'h1_tags': h1_tags,
            'image_alt_texts': image_alt_texts,
            'page_speed': page_speed_data
        }

        return jsonify(seo_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
