import sys
import matplotlib.pyplot as plt
import average
import boundingtoposition


def main(file, src):
    players = load_players(file, src)
    players = average.process_all(players, 30, 12)
    plot_players(players)


def load_players(file, src):
    points2 = boundingtoposition.setup(src)
    players = boundingtoposition.projection(file,
                                            "../calibration_matrix.yaml",
                                            points2)
    return players


def plot_players(players, fontsize=22):
    plt.rcParams.update({'font.size': fontsize})
    for player in players:
        plt.plot(player[1][1], player[1][2], color="blue")
    plt.xlabel("x position")
    plt.ylabel("y position")
    plt.show()


if "__name__" == "__main__":
    main(sys.argv[1])
