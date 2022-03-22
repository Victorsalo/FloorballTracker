from math import sqrt
import numpy as np
import csv
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


def estimate_acceleration(speeds, fps):
    """
    Estimates the acceleration of an object given its speeds at diffrent
    times and their recording speed.

    Arguments:
    speeds -- the speeds of the object.
    fps -- The speed at which the points were recorded.
    """

    accelerations = np.zeros(len(speeds))
    deltat = 1/fps
    for i in range(len(speeds)-1):
        accelerations[i] = (speeds[i+1]-speeds[i])/deltat
    # accelerations[-1] = accelerations[-2]
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
    for player in all_player_data:
        xs = moving_average(player[1][1], 6)
        ys = moving_average(player[1][2], 6)
        speeds = estimate_speed(xs, ys, fps)
        accelerations = estimate_acceleration(speeds, fps)
        processed_players.append([player[0], [player[1][0],
                                  xs, ys, speeds, accelerations]])
    return processed_players
#[round(x, 0) for x in values]
#[[playernumber, [[frame,], [x,], [y,], [speed,], [acceleration,]]],]
def round_data(values):
    for i in range(len(values)):
        for j in range(len(values[i][1])):
            for k in range(len(values[i][1][j])):
                values[i][1][j][k] = round(values[i][1][j][k], 2)
    return values





def write_to_file(processed_players):
    """
    Writes the output of process_all() to a csv-file.

    Arguments:
    processed_players -- Output of process_all().
    """

    for player in processed_players:
        with open(f"player{player[0]}.csv", 'w',
                  encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(player[1])


def test():
    import matplotlib.pyplot as plt
    from math import sin, pi
    xs = np.linspace(0, 2*pi*10, 200)
    ys = [sin(x) for x in xs]
    ys = estimate_speed(xs, ys, 30)
    plt.plot(xs, ys)
    plt.show()
