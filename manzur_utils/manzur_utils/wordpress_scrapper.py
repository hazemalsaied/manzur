import pandas as pd
import requests


def scrap_posts(site_name):
    api_url = f'https://{site_name}/wp-json/wp/v2/posts?page='
    for i in range(1, 40000):
        response = requests.get(api_url + str(i))
        if not posts.empty and len(posts) % 200 == 0:
            posts.to_pickle('posts.pkl')
        if response.status_code == 200:
            for post in response.json():
                posts = posts.append(post, ignore_index=True)
        else:
            posts.to_pickle('posts.pkl')
            break


def scrap_tags(site_name, item_type='categories'):
    items = pd.DataFrame()
    for i in range(1, 4000):
        api_cats_url = f'https://{site_name}/wp-json/wp/v2/{item_type}?page=' + str(i)
        response = requests.get(api_cats_url)
        if not items.empty and len(items) % 500 == 0:
            items.to_pickle(f'{item_type}.pkl')
        if response.status_code == 200:
            if not response.json():
                break
            for item in response.json():
                items = items.append(item, ignore_index=True)
        else:
            break
    items.to_pickle(f'{item_type}.pkl')
    return items
