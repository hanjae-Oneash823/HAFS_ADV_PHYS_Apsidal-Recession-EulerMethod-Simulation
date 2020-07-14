import numpy as np
import matplotlib as mpl
import math
import matplotlib.pyplot as plt
import matplotlib.animation as anim

mpl.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg-4.3-win64-static\bin\ffmpeg.exe'

# Settings
time_interval = 0.01
number_of_cycles = int(input("Input number of desired cycles: "))

# Constants
# G = 6.67408 * math.pow(10, -11)
# M = 1.989 * math.pow(10, 30)
G, M = 1, 1

# initial conditions
initial_x = 4
initial_y = 0
raw_initial_vx = 0
raw_initial_vy = 1.7
initial_r = math.sqrt(math.pow(initial_x, 2) + math.pow(initial_y, 2))  # sqrt(x^2+y+2)
initial_vx = raw_initial_vx - (time_interval/2)*(G * M * initial_x)/math.pow(initial_r, 3)  # half of an interval ahead
initial_vy = raw_initial_vy - (time_interval/2)*(G * M * initial_y)/math.pow(initial_r, 3)  # half of an interval ahead


# Defining Arrays
x_array = np.array([initial_x])
y_array = np.array([initial_y])
vx_array = np.array([initial_vx])
vy_array = np.array([initial_vy])


# Defining Functions


def position_next(p, v, t):
    n = p + t * v
    return n


def velocity_next(x, y, v):
    r = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    n = v - (G * M * x)/math.pow(r, 3)
    return n


def last_value_of(array):
    length = len(array)
    return array[length-1]


# Calculations
cycle_count = 1
while cycle_count <= number_of_cycles:
    x = position_next(last_value_of(x_array), last_value_of(vx_array), time_interval)
    y = position_next(last_value_of(y_array), last_value_of(vy_array), time_interval)
    x_array = np.append(x_array, [x])
    y_array = np.append(y_array, [y])
    vx = velocity_next(x, y, last_value_of(vx_array))
    vy = velocity_next(y, x, last_value_of(vy_array))
    vx_array = np.append(vx_array, [vx])
    vy_array = np.append(vy_array, [vy])
    cycle_count += 1


# Test Area
print(x_array)
print(y_array)


fig = plt.figure()


def animate(i, fig, scat):
    scat.set_offsets(([0, 0], [x_array[i - 1], y_array[i - 1]]))
    print('Frames: %d' %i)

    return scat,


ax = fig.add_subplot(111)
ax.grid(True)
plt.axes(xlim=(-6, 6), ylim=(-6, 6))
scat = plt.scatter([0, 0], [0, 0])
scat.set_alpha(0.8)

animation = anim.FuncAnimation(fig, animate, fargs=(fig, scat), frames=number_of_cycles, interval=1, repeat=True, blit=True)

plt.show()

f = r"C://Users/hanja/Desktop/animation.mp4"
writervideo = animation.FFMpegWriter(fps=60)
animation.save(f, writer=writervideo)
