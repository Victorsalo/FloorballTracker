from math import sqrt
import os
import csv
import numpy as np
from scipy.ndimage.filters import uniform_filter1d


def moving_average(points, smoothing):
    """
    Takes the moving average of points and smooths each element with the
    smoothing surrounding elements.

    Keyword arguments:
    points -- The list of points to be smoothed.
    smoothing -- The amount of smoothing to be done.
    """

    return uniform_filter1d(points, size=smoothing, mode="nearest")


# TODO: Change to a better speed formula.
def estimate_speed(xs, ys, fps):
    """
    Estimates the speed of an object given its cordinates and their
    recording speed. Uses instantanious speed.

    TODO: Change to a better way of calculating the speed.

    Keyword arguments:
    xs -- The x positions of the object.
    ys -- The y positions of the object.
    fps -- The speed at which the points were recorded.
    """

    speeds = np.zeros(len(xs))
    deltat = 1/fps
    for i in range(len(xs)-1):
        dist = sqrt((xs[i+1]-xs[i])**2 + (ys[i+1]-ys[i])**2)
        speeds[i] = dist/deltat
    speeds[-1] = speeds[-2]
    return speeds


def estimate_acceleration(xs, ys, fps):
    """
    Estimates the acceleration of an object given its speeds at diffrent
    times and their recording speed.

    Arguments:
    speeds -- the speeds of the object.
    fps -- The speed at which the points were recorded.
    """

    accelerations = np.zeros(len(xs))
    deltat = 1/fps
    for i in range(2, len(xs)-1):
        xacc = (xs[i+1]-2*xs[i]+xs[i-1])/(deltat**2)
        yacc = (ys[i+1]-2*ys[i]+ys[i-1])/(deltat**2)
        accelerations[i] = sqrt(xacc**2+yacc**2)
    return accelerations


def process_all(all_player_data, fps):
    """
    Uses data on the form [[playernumber, [[frame,], [x,], [y,]]],] to obtain
    a smoothed out version along with the speed and acceleration. Data is
    returned with the form
    [[playernumber, [[frame,], [x,], [y,], [speed,], [acceleration,]]],]

    Arguments:
    all_player_data -- Player data on the form
                       [[playernumber, [[frame,], [x,], [y,]]],]
    fps -- The speed at which the points were recorded.
    """

    processed_players = []
    smoothing = 6
    for player in all_player_data:
        xs = moving_average(player[1][1], smoothing)
        ys = moving_average(player[1][2], smoothing)
        speeds = estimate_speed(xs, ys, fps)
        accelerations = estimate_acceleration(xs, ys, fps)
        processed_players.append([player[0], [player[1][0],
                                  xs, ys, speeds, accelerations]])
    return processed_players


# [round(x, 0) for x in values]
# [[playernumber, [[frame,], [x,], [y,], [speed,], [acceleration,]]],]
def round_data(values):
    for i in range(len(values)):
        for j in range(len(values[i][1])):
            for k in range(len(values[i][1][j])):
                values[i][1][j][k] = round(values[i][1][j][k], 2)
    return values


def write_to_file(processed_players, directory):
    """
    Writes the output of process_all() to a csv-file.

    Arguments:
    processed_players -- Output of process_all().
    """

    taken = set()
    rounded_players = round_data(processed_players)
    for player in rounded_players:
        id = player[0]
        while id in taken:
            id += 100
        name = f"player{id}.csv"
        fpath = os.path.join(directory, name)
        with open(fpath, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(player[1])
        taken.add(id)


def test():
    import matplotlib.pyplot as plt
    from math import sin, pi
    xs = np.linspace(0, 2*pi*10, 200)
    ys = [sin(x) for x in xs]
    ys = estimate_speed(xs, ys, 30)
    plt.plot(xs, ys)
    plt.show()
