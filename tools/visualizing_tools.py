import numpy as np
import itertools
from matplotlib import pyplot as plt

# Source for distinct colors https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
colors = np.array([
    [230, 25, 75],
    [60, 180, 75],
    [255, 225, 25],
    [67, 99, 216],
    [245, 130, 49],
    [145, 30, 180],
    [70, 240, 240],
    [240, 50, 230],
    [188, 246, 12],
    [250, 190, 190],
    [0, 128, 128],
    [230, 190, 255],
    [154, 99, 36],
    [255, 250, 200],
    [128, 0, 0],
    [170, 255, 195],
    [128, 128, 0],
    [255, 216, 177],
    [0, 0, 117],
    [128, 128, 128],
    [255, 255, 255],
    [0, 0, 0]
]).astype(np.float)
colors = colors / 255.


def plot_histogram(pos_features, neg_features, pos_labels='Knowns', neg_labels='Unknowns', title="Histogram",
                   file_name='{}foo.pdf'):
    """
    This function plots the Histogram for Magnitudes of feature vectors.
    """
    pos_mag = np.sqrt(np.sum(np.square(pos_features), axis=1))
    neg_mag = np.sqrt(np.sum(np.square(neg_features), axis=1))

    pos_hist = np.histogram(pos_mag, bins=500)
    neg_hist = np.histogram(neg_mag, bins=500)

    fig, ax = plt.subplots(figsize=(4.5, 1.75))
    ax.plot(pos_hist[1][1:], pos_hist[0].astype(np.float16) / max(pos_hist[0]), label=pos_labels, color='g')
    ax.plot(neg_hist[1][1:], neg_hist[0].astype(np.float16) / max(neg_hist[0]), color='r', label=neg_labels)

    ax.tick_params(axis='both', which='major', labelsize=12)

    plt.xscale('log')
    plt.tight_layout()
    if title is not None:
        plt.title(title)
    plt.savefig(file_name.format('Hist', 'pdf'), bbox_inches='tight')
    plt.show()


def plotter_2D(
        pos_features,
        labels,
        neg_features=None,
        pos_labels='Knowns',
        neg_labels='Unknowns',
        title=None,
        file_name='foo.pdf',
        final=False,
        pred_weights=None,
        heat_map=False):
    global colors
    plt.figure(figsize=[6, 6])

    if heat_map:
        min_x, max_x = np.min(pos_features[:, 0]), np.max(pos_features[:, 0])
        min_y, max_y = np.min(pos_features[:, 1]), np.max(pos_features[:, 1])
        x = np.linspace(min_x * 1.5, max_x * 1.5, 200)
        y = np.linspace(min_y * 1.5, max_y * 1.5, 200)
        pnts = list(itertools.chain(itertools.product(x, y)))
        pnts = np.array(pnts)

        e_ = np.exp(np.dot(pnts, pred_weights))
        e_ = e_ / np.sum(e_, axis=1)[:, None]
        res = np.max(e_, axis=1)

        plt.pcolor(x, y, np.array(res).reshape(200, 200).transpose(), rasterized=True)

    if neg_features is not None:
        # Remove black color from knowns
        colors = colors[:-1, :]

    # TODO:The following code segment needs to be improved
    colors_with_repetition = colors.tolist()
    for i in range(int(len(set(labels.tolist())) / colors.shape[0])):
        colors_with_repetition.extend(colors.tolist())
    colors_with_repetition.extend(colors.tolist()[:int(colors.shape[0] % len(set(labels.tolist())))])
    colors_with_repetition = np.array(colors_with_repetition)
    print(colors_with_repetition.shape, len(set(labels.tolist())))

    plt.scatter(pos_features[:, 0], pos_features[:, 1], c=colors_with_repetition[labels.astype(np.int)],
                edgecolors='none', s=0.5)
    if neg_features is not None:
        plt.scatter(neg_features[:, 0], neg_features[:, 1], c='k', edgecolors='none', s=15, marker="*")
    if final:
        plt.gca().spines['right'].set_position('zero')
        plt.gca().spines['bottom'].set_position('zero')
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.tick_params(axis='both', bottom=False, left=False, labelbottom=False, labeltop=False, labelleft=False,
                        labelright=False)
        plt.axis('equal')

    plt.savefig(file_name.format('2D_plot', 'png'), bbox_inches='tight')
    plt.show()
    if neg_features is not None:
        plot_histogram(pos_features, neg_features, pos_labels=pos_labels, neg_labels=neg_labels, title=title,
                       file_name=file_name)