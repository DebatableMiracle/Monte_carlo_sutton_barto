import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch

def draw_grid(track, layers=None, paths=None, ax=None, title=None, cell=0.4):
    """
    track  : (H, W) bool array, True = drivable, False = wall
    layers : {"name": (list_of_(x, y)_cells, color)}  drawn in order, later wins
    paths  : {"name": (list_of_(x, y)_cells, color)}  drawn as lines on top
    """
    h, w = track.shape
    if ax is None:
        _, ax = plt.subplots(figsize=(w * cell + 1, h * cell + 1))

    # build the RGB image: track -> white, wall -> dark grey, then layers
    img = np.empty((h, w, 3))
    img[track] = to_rgb("white")
    img[~track] = to_rgb("#3a3a3a")
    for cells, color in (layers or {}).values():
        for x, y in cells:
            img[y, x] = to_rgb(color)
    ax.imshow(img, origin="upper", interpolation="nearest")

    # paths (e.g. trajectories), with markers at each visited cell
    for cells, color in (paths or {}).values():
        xs, ys = zip(*cells)
        ax.plot(xs, ys, "-o", color=color, ms=4, lw=1.5)

    # grid lines on cell EDGES, labels on cell CENTERS
    ax.set_xticks(range(w))
    ax.set_yticks(range(h))
    ax.set_xticks(np.arange(-0.5, w, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, h, 1), minor=True)
    ax.grid(which="minor", color="#bbbbbb", lw=0.5)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(labelsize=7)
    ax.set_xlim(-0.5, w - 0.5)
    ax.set_ylim(h - 0.5, -0.5)  # y=0 at top, like the book figure

    # legend from layer + path names
    handles = [Patch(facecolor=c, edgecolor="k", label=n)
               for n, (_, c) in {**(layers or {}), **(paths or {})}.items()]
    if handles:
        ax.legend(handles=handles, loc="upper left",
                  bbox_to_anchor=(1.01, 1), fontsize=8)
    if title:
        ax.set_title(title)
    return ax