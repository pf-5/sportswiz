from bs4 import BeautifulSoup
import requests
import reutils
from utils import response


cache_data = {}


def lambda_handler(event, context):

    # read query
    params = event.get('queryStringParameters') or {}
    provider = params.get('provider')
    sport = params.get('sport') or ''
    query = params.get('query') or ''
    if not provider:
        return response({'error': 'invalid query parameters'}, status=400)

    provider = provider.lower()
    sport = sport.lower()

    if provider == 'crackstreams' and sport == 'mlb':
        link = crackstreams_mlb(query)
        if link:
            return response({'link': link})
        else:
            return response({'error': 'stream not found'})

    return response({'error': 'invalid provider'})


def fetch_page(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    return soup


def crackstreams_mlb(query):

    def fetch():
        soup = fetch_page('https://crackstreams.biz/mlbstreams/')
        stream_pages = []
        for page in soup.select('.ctpage'):
            teams_text = page.select_one('.media-heading').text
            teams = reutils.clean_spacing(
                reutils.alphanumeric(teams_text)).lower()
            anchor = page.select_one('a')
            link = anchor.attrs['href']
            stream_pages.append({
                'teams': teams,
                'link': link,
            })
        cache_data['crackstreams_mlb'] = stream_pages
        return stream_pages

    stream_pages = cache_data.get('crackstreams_mlb') or fetch()
    query = query.strip().lower()
    query_words = query.split(' ')
    for page in stream_pages:
        if any([q in page['teams'] for q in query_words]):
            return page['link']
