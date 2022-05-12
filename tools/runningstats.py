import sys
import matplotlib.pyplot as plt
import average
import boundingtoposition


def main(file, src):
    players = load_players(file, src)
    players = average.process_all(players, 30, 20)
    plot_players(players)
    plot_speeds(players)
    plot_accelerations(players)
    return players


# Points from testvideo.
# points1 = [(0,0), (5.9, 0), (5.9, 5.1), (0, 5.1)]
def load_players(file, src, points1=None):
    points2 = boundingtoposition.setup(src)
    players = boundingtoposition.projection(file,
                                            "../calibration_matrix.yaml",
                                            points2,
                                            points1)
    return players


def setup_plots_pgf():
    options = {
                "text.usetex": True,
                "font.family": "serif",
                "font.serif": [],
                "font.sans-serif": [],
                "font.monospace": [],
                "axes.labelsize": 10,
                "font.size": 10,
                "legend.fontsize": 8,
                "xtick.labelsize": 8,
                "ytick.labelsize": 8,
                "figure.figsize": r"0.45\textwidth",
                "pgf.preamble": "\n".join([
                    r"\usepackage[utf8]{inputenc}",
                    r"\usepackage[T1]{fontenc}",
                    r"\usepackage[detect-all,locale=DE]{siunitx}",
                    r"\usepackage{siunitx}",
                    ]),
                "text.latex.preamble": r"\usepackage{siunitx}"
        }
    plt.rcParams.update(options)


def setup_plots():
    options = {
                "text.usetex": True,
                "font.family": "serif",
                "axes.labelsize": 20,
                "xtick.labelsize": 18,
                "ytick.labelsize": 18,
                "font.size": 20,
                "text.latex.preamble": r"\usepackage{siunitx}"
        }
    plt.rcParams.update(options)


def plot_players(players, fontsize=22, save=None):
    setup_plots()
    for player in players:
        plt.plot(player[1][1], player[1][2], color="blue")
    plt.xlabel(r"$x$ position [\si{m}]")
    plt.ylabel(r"$y$ position [\si{m}]")
    plt.tight_layout()
    if save is not None:
        plt.savefig(save, backend="pgf")
    plt.show()


def plot_speeds(players, fontsize=22, save=None):
    setup_plots()
    for player in players:
        plt.plot(player[1][0], player[1][3], color="blue")
    plt.xlabel(r"Bildruta")
    plt.ylabel(r"Fart [\si{ms^{-1}}]")
    plt.tight_layout()
    if save is not None:
        plt.savefig(save, backend="pgf")
    plt.show()


def plot_accelerations(players, fontsize=22, save=None):
    setup_plots()
    for player in players:
        plt.plot(player[1][0], player[1][4], color="blue")
    plt.xlabel(r"Bildruta")
    plt.ylabel(r"Accelerationens belopp [\si{ms^{-2}}]")
    plt.tight_layout()
    if save is not None:
        plt.savefig(save, backend="pgf")
    plt.show()


if "__name__" == "__main__":
    main(sys.argv[1], sys.argv[2])
