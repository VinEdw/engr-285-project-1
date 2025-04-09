import stream_plotter as sp

def y_prime(x, y, a, b):
    return -a*y + b*x*y

def x_prime(x, y, c, d):
    return d*x - c*y*x

board_size = 80 * 90
points = 1000
padding = 10

x_min = -padding
x_max = board_size + padding
x_points = points

y_min = -padding
y_max = board_size + padding
y_points = points

a = 1100
b = 1
c = 1
d = 550

y_diff = lambda x, y: y_prime(x, y, a, b)
x_diff = lambda x, y: x_prime(x, y, c, d)

fig, ax = sp.create_stream_plot(x_min, x_max, x_points, y_min, y_max, y_points, y_diff, x_diff)
ax.set(xlabel="Fish Population", ylabel="Shark Population")
fig.savefig("media/lvm_stream_plot.svg")
