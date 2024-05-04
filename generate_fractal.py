import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import numpy as np

def draw_koch_snowflake(order, size):
    def koch_curve(start, end, order):
        if order == 0:
            return [start, end]
        else:
            delta = (end - start) / 3
            p1 = start + delta
            p2 = p1 + delta * np.exp(-np.pi / 3 * 1j)
            p3 = start + 2 * delta
            return (
                koch_curve(start, p1, order - 1)[:-1] +
                koch_curve(p1, p2, order - 1)[:-1] +
                koch_curve(p2, p3, order - 1)[:-1] +
                koch_curve(p3, end, order - 1)
            )

    vertices = [size * np.exp(2 * np.pi * 1j * i / 3) for i in range(3)]
    snowflake_points = []
    for i in range(3):
        snowflake_points += koch_curve(vertices[i], vertices[(i + 1) % 3], order)
    snowflake_points.append(snowflake_points[0])
    snowflake_points = np.array(snowflake_points)

    x = np.real(snowflake_points)
    y = np.imag(snowflake_points)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = mcoll.LineCollection(segments, cmap=plt.get_cmap('viridis'), linewidths=2)
    lc.set_array(np.linspace(0, 1, len(segments)))

    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.axis('equal')
    ax.axis('off')
    plt.savefig('snowflake.png', bbox_inches='tight', pad_inches=0, transparent=True)
    return snowflake_points
