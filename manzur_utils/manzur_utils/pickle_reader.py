import html2text
import pandas as pd

site_data_path = '/Users/hazem/Documents/manzur/data/pickles/enabbaladi/scrapped/'
site_preprocessed_data_path = '/Users/hazem/Documents/manzur/data/pickles/enabbaladi/preprocessed/'
abstract_cats = {
    'Syria': ['66'],
    'Politics': ['11374', '1040', '31', '54077'],
    'Economy': ['11378', '1039', '11379', '11512', '11380', '89388'],
    'Society': ['6813', '1208', '11384', '381', '389', '89769', '1042'],
    'Culture': ['43657', '11376', '14', '1043', '11387', '386', '13', '56383'],
    'Human_rights': ['89389', '89387', '23', '6', '54078'],
    'Syrian_exode': ['11377', '11373', '70035', '52951'],
    'Opinion': ['1041', '11734', '1834', '70', '28563'],
    'Life_style': ['10981', '53', '54076', '89789', '95030', '34'],
    'Technologies': ['27', '89793', '11386', '11383'],
    'In_English': ['11385', '48'],
    'Personal_development': ['43658', '51763', '11381', '89790', '5763', '11375', '51764'],
    'Others': ['47304', '1045', '82228', '51762', '382', '11', '50952', '95029', '382', '11'],
    'Multimedia': ['2853', '73564', '42554', '10821', '11357', '1045', '1183', '82228'],
    'Sports': ['5235', '11511', '11510', '47116', '95031']
}


def picklize(posts, path, file_size=5000):
    for i in range(int(len(posts) / file_size) + 1):
        end = (i + 1) * file_size if (i + 1) * file_size < len(posts) else len(posts)
        posts[i * file_size: end].to_pickle(path + f'posts_1_{i}.pkl')


def read_preprocessed_data(post_file_num, tag_file_num):
    tags = read_tags(tag_file_num)
    file = site_data_path + 'categories.pkl'
    categories = read_tags_file(file)
    posts = list()
    for i in range(post_file_num):
        file = site_preprocessed_data_path + f'posts/posts_1_{i}.pkl'
        posts.append(pd.read_pickle(file))
    posts = pd.concat(posts)
    return posts, tags, categories


def read_all_data(post_file_num, tag_file_num):
    tags = read_tags(tag_file_num)
    file = site_data_path + 'categories.pkl'
    categories = read_tags_file(file)
    posts = read_posts(post_file_num, tags, categories, site_data_path)
    posts['abstract_cats'] = posts['categories'].apply(_get_abstract_cats)
    for w in ['Others', 'Multimedia', 'Syria']:
        posts['abstract_cats'] = posts['abstract_cats'].str.replace(f'|{w}', '', regex=False)
        posts['abstract_cats'] = posts['abstract_cats'].str.replace(f'{w}|', '', regex=False)
    posts.loc[(posts['abstract_cats'] == ''), 'abstract_cats'] = 'Politics'
    return posts, tags, categories


def read_posts(post_file_num, tags, cats, path):
    posts = list()
    for i in range(post_file_num):
        file = path + f'posts/posts_1_{i}.pkl'
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
        if counts.get(k, 0) >= 1:
            tags[k.strip()] = {'name': names[k], 'count': int(counts.get(k, 0))}
    return tags


def _get_abstract_cats(cats):
    abs_cats = set()
    for c in cats:
        if c:
            for abst_cat, abst_cat_subcats in abstract_cats.items():
                if str(c) in abst_cat_subcats:
                    abs_cats.add(abst_cat)
    return '|'.join(abs_cats)
