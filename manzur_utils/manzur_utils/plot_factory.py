import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer
from .pickle_reader import abstract_cats
import arabic_reshaper
from bidi.algorithm import get_display


def plot_abstract_category(posts, normalize=True):
    cat_counts_dict = dict()
    for c in abstract_cats:
        posts_len = len(posts[posts['abstract_cats'].str.contains(c, regex=False)])
        # posts_len = len(posts[posts['abstract_cats'] == c])
        cat_counts_dict[c] = posts_len / (len(posts) if normalize else 1)
    cat_counts_dict = {k: v for k, v in sorted(cat_counts_dict.items(), key=lambda x: x[1])}
    cat_labels, cat_counts = list(cat_counts_dict.keys()), list(cat_counts_dict.values())
    _plot_barh(cat_labels, cat_counts, normalize=normalize)


def plot_tags_timeline(posts, column='abstract_cats'):
    mlb = MultiLabelBinarizer()
    mlb.fit_transform(posts[column].str.split('|'))
    cats = list(mlb.classes_)
    posts['grouping_date'] = posts['date_gmt'].apply(lambda x: x[:7])
    months, cats_freq = list(), dict()
    for mth_year, df in posts.groupby('grouping_date'):
        months.append(mth_year)
        df[column] = df[column].astype(str)
        cats_freq[mth_year] = dict()
        for cat in cats:
            cats_freq[mth_year][cat] = len(df[df[column].str.contains(cat, regex=False)])
    for cat in cats:
        cat_freq_list = list()
        for mth in months:
            cat_freq_list.append(cats_freq[mth].get(cat))
        _plot_line(months, cat_freq_list, title=cat)


def _plot_line(xs, ys, title='', figsize=(15, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(range(len(xs)), ys)
    ax.set_xticks(range(len(xs)))
    labels = list()
    for x in xs:
        if int(x[-2:]) % 2 == 0:
            labels.append(x)
        else:
            labels.append('')
    ax.set_xticklabels(labels, rotation='vertical')
    title = get_display(arabic_reshaper.reshape(title))
    ax.set_title(title)
    fig.tight_layout()
    plt.show()


def _plot_barh(cat_labels, cat_counts, figsize=(10, 10), normalize=True):
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(range(len(cat_labels)), cat_counts, width, color=mcolors.TABLEAU_COLORS)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_yticks(range(len(cat_labels)))
    ax.set_yticklabels(cat_labels)
    for i in range(len(cat_labels)):
        value = str(round(100 * cat_counts[i], 1)) if normalize else cat_counts[i]
        ax.text(cat_counts[i], i, value, ha='center', va='center')

    fig.tight_layout()
    plt.show()
