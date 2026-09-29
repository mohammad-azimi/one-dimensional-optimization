"""Scientific plots; these objective calls are outside all search counters."""
from pathlib import Path


def make_plots(function, payload, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    output = Path(output)
    meta, results = payload["problem"], payload["results"]
    a, b = meta["a"], meta["b"]
    colors = ["#2375A9", "#4B917D", "#D58A31", "#955DA4", "#C05255"]
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.dpi": 160})
    xs = np.linspace(a, b, 1401)
    ys = [function(float(x)) for x in xs]
    fig, ax = plt.subplots(figsize=(8, 4.2), layout="constrained")
    ax.plot(xs, ys, color=colors[0], linewidth=2)
    if meta["reference_x"] is not None and a <= meta["reference_x"] <= b:
        ref = meta["reference_x"]
        ax.scatter([ref], [function(ref)], color=colors[4], zorder=3)
        ax.annotate("Exact minimum", (ref, function(ref)),
                    xytext=(20, 28), textcoords="offset points",
                    arrowprops={"arrowstyle": "->", "color": "#555555"})
    ax.set(xlabel="x", ylabel="f(x)", title="Objective function on the selected interval")
    ax.grid(alpha=0.2)
    fig.savefig(output / "objective.png")
    plt.close(fig)

    methods = list(dict.fromkeys(r["method"] for r in results))
    fig, ax = plt.subplots(figsize=(8, 4.2), layout="constrained")
    for color, name in zip(colors, methods):
        rows = [r for r in results if r["method"] == name]
        ax.plot([r["delta"] for r in rows],
                [r["total_evaluations"] for r in rows],
                marker="o", label=name, color=color)
    ax.set(xscale="log", yscale="log", xlabel="Requested absolute x error (delta)",
           ylabel="Objective evaluations including final report",
           title="Function evaluations required by each method")
    ax.invert_xaxis()
    ax.grid(alpha=0.2, which="both")
    ax.legend(fontsize=9)
    fig.savefig(output / "evaluations.png")
    plt.close(fig)

    finest = min(meta["deltas"])
    rows = [r for r in results if r["delta"] == finest]
    fig, ax = plt.subplots(figsize=(8, 3.6), layout="constrained")
    for i, (color, row) in enumerate(zip(colors, rows)):
        ax.plot([row["left"], row["right"]], [i, i],
                linewidth=4, color=color)
        ax.plot(row["x"], i, "o", color="black", markersize=4)
    if meta["reference_x"] is not None:
        ax.axvline(meta["reference_x"], color="#555555", linestyle="--",
                   label="Exact minimum")
        ax.legend(fontsize=9)
    ax.set(yticks=range(len(rows)), yticklabels=[r["method"] for r in rows],
           xlabel="x", title=f"Final brackets and midpoints at delta = {finest:g}")
    ax.ticklabel_format(axis="x", useOffset=False)
    ax.grid(axis="x", alpha=0.2)
    fig.savefig(output / "validation.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.1), layout="constrained")
    for color, row in zip(colors[2:], rows[2:]):
        history = row["history"]
        ax.step([h[0] for h in history], [h[2] - h[1] for h in history],
                where="post", label=row["method"], color=color)
    ax.axhline(2 * finest, color="#666666", linestyle="--",
               label="Target width = 2 delta")
    ax.set(yscale="log", xlabel="Search evaluations", ylabel="Bracket width",
           title="Interval reduction during the finest search")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.2)
    fig.savefig(output / "convergence.png")
    plt.close(fig)
