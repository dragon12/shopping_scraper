import requests
import re
import bs4
from multiprocessing import Pool


root_url = 'http://pyvideo.org'
index_url = root_url + '/category/50/pycon-us-2014'


def get_video_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)
    return [a.attrs.get('href') for a in soup.select(
            'div.video-summary-data a[href^=/video]')]


def get_video_data(video_page_url):
    print "getting data from", video_page_url
    video_data = {}
    response = requests.get(root_url + video_page_url)
    soup = bs4.BeautifulSoup(response.text)
    video_data['title'] = soup.select('div#videobox h3')[0].get_text()
    video_data['speakers'] = [
        a.get_text() for a in soup.select('div#sidebar a[href^=/speaker]')]

    youtube_links = soup.select(
        'div#sidebar a[href^=http://www.youtube.com]')

    if (not youtube_links):
        return video_data

    video_data['youtube_url'] = youtube_links[0].get_text()

    soup = bs4.BeautifulSoup(requests.get(video_data['youtube_url']).text)

    view_count_select = soup.select('div.watch-view-count')
    video_data['view_count'] = int(
        re.sub(
            '[^\d]',
            '',
            view_count_select[0].text))

    likes_dislikes_select = soup.select('span#watch-like-dislike-buttons')[0]
    likes_dislikes_button_select = likes_dislikes_select.select('span.yt-uix-button-content')

    video_data['likes'] = int(re.sub(
        '[^\d]', '', likes_dislikes_button_select[0].get_text()))

    video_data['dislikes'] = int(re.sub(
        '[^\d]', '', likes_dislikes_button_select[2].get_text()))

    return video_data


def show_video_stats():
    pool = Pool(8)
    urls = get_video_page_urls()

    results = pool.map(get_video_data, urls)
    # results = map(get_video_data, urls)
    return results

video_stats = show_video_stats()

print """stats:
%s
""" % video_stats
