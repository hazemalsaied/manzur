import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from .pickle_reader import abstract_cats


def plot_abstract_category(posts, normalize=True):
    cat_counts_dict = dict()
    for c in abstract_cats:
        posts_len = len(posts[posts['abstract_cats'].str.contains(c, regex=False)])
        # posts_len = len(posts[posts['abstract_cats'] == c])
        cat_counts_dict[c] = posts_len / (len(posts) if normalize else 1)
    cat_counts_dict = {k: v for k, v in sorted(cat_counts_dict.items(), key=lambda x: x[1])}
    cat_labels, cat_counts = list(cat_counts_dict.keys()), list(cat_counts_dict.values())
    _plot_barh(cat_labels, cat_counts, normalize=normalize)


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
