import pandas as pd
import html2text

site_data_path = '/Users/hazem/Documents/manzur/data/pickles/enabbaladi/'


def read_all_data(post_file_num, tag_file_num):
    tags = read_tags(tag_file_num)
    file = site_data_path + 'categories.pkl'
    categories = read_tags_file(file)
    posts = read_posts(post_file_num, tags, categories)
    return posts, tags, categories


def read_posts(post_file_num, tags, cats):
    posts = list()
    for i in range(post_file_num):
        file = site_data_path + f'posts/posts_1_{i}.pkl'
        cleaned_posts = clean_post_file(file, tags, cats)
        posts.append(cleaned_posts)
    return pd.concat(posts)


def read_tags(tag_file_num=9):
    tags = dict()
    for i in range(tag_file_num):
        file = site_data_path + f'tags/tag_{i}.pkl'
        new_tags = read_tags_file(file)
        tags = {**tags, **new_tags}
    return tags


def clean_post_file(file, tags, cats):
    h = html2text.HTML2Text()
    h.ignore_links = True
    df = pd.read_pickle(file)
    df['title'] = df['title'].apply(lambda x: dict(x)['rendered'].strip())
    df['title'] = df['title'].apply(h.handle)
    df['content'] = df['content'].apply(lambda x: dict(x)['rendered'])
    df['html_content'] = df['content']
    df['content'] = df['content'].apply(h.handle)
    df['content'] = df['content'].str.replace('\n', ' ')
    df['excerpt'] = df['excerpt'].apply(lambda x: dict(x)['rendered'])
    df['excerpt'] = df['excerpt'].apply(h.handle)
    df['tags_str'] = df['tags'].apply(
        lambda x: '|'.join([tags.get(str(e), dict()).get('name', str(e)) for e in list(x)]))
    df['categories_str'] = df['categories'].apply(
        lambda x: '|'.join([cats.get(str(e), dict()).get('name', str(e)) for e in list(x)]))
    df['author'] = df['author'].apply(int).apply(str)
    df['id'] = df['id'].apply(int).apply(str)
    df['related_posts'] = df['jetpack-related-posts'].apply(lambda x: '|'.join([str(e['id']) for e in list(x)]))

    return df[['id', 'title', 'content', 'html_content', 'excerpt', 'categories', 'author', 'date_gmt',
               'tags', 'tags_str', 'categories_str', 'related_posts']]


def read_tags_file(file):
    tags = dict()
    df = pd.read_pickle(file)
    df['id'] = df['id'].apply(int)
    df['id'] = df['id'].apply(str)
    df = df[['id', 'name', 'count']]
    df = df.set_index('id')
    names = df.to_dict()['name']
    counts = df.to_dict()['count']
    for k in names:
        if counts.get(k,0) >=1:
            tags[k.strip()] = {'name': names[k], 'count': int(counts.get(k,0))}
    return tags
