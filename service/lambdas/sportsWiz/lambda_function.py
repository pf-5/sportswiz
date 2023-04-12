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

    if provider == 'crk' and sport == 'mlb':
        link = crackstreams_mlb(query)
        return response({'link': link}) if link else response({'error': 'stream not found'})
    elif provider == 'ddl':
        link = ddl_sport_streams(sport, query)
        return response({'link': link}) if link else response({'error': 'stream not found'})

    return response({'error': 'invalid provider'}, status=400)


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


def ddl_sport_streams(sport, query):

    def get_stream_number(href):
        try:
            stream_number = href.rsplit('-', 1)[1].rsplit('.')[0]
            return str(int(stream_number))
        except:
            return None

    def fetch():
        soup = fetch_page('https://daddylivehd.sx/')
        stream_pages = []
        for span in soup.select('span'):
            anchor = span.select_one('a')
            if anchor:
                if '/stream/' in anchor['href'] or '':
                    title = span.previous_sibling.text
                    title = reutils.clean_spacing(
                        reutils.alphanumeric(title)).lower()
                    stream_number = get_stream_number(anchor['href'])
                    if stream_number:
                        stream_pages.append({
                            'title': title,
                            'stream': 'https://daddylivehd.sx/embed/stream-%s.php' % stream_number,
                        })
        cache_data['ddl_sport_streams'] = stream_pages
        return stream_pages

    stream_pages = cache_data.get('ddl_sport_streams') or fetch()
    query = query.strip().lower()
    query_words = query.split(' ')
    for page in stream_pages:
        if sport.lower() in page['title']:
            if any([q in page['title'] for q in query_words]):
                return page['stream']
