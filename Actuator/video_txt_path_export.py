import matplotlib.pyplot as plt
import numpy as np
import sys
import math


def read_point_trajectory_data(file_path):
    time = []
    x_values = []
    y_values = []

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
        print(f"Number of lines read: {len(lines)}")
        for line in lines:
            if line.strip() and not line.startswith('#'):
                try:
                    t, x, y = map(float, line.split())
                    # print('time, position x, position y:', t, x, y)
                    time.append(t)
                    x_values.append(-x)
                    y_values.append(y)
                except ValueError:
                    # Skip lines that cannot be converted to float (e.g., headers)
                    pass

    return time, x_values, y_values


def read_arrow_trajectory_data(file_path, base_str: str, arrow_str: str,):
    time_base_ms, base_x_values, base_y_values = [], [], []
    time_arrow_ms, arrow_x_values, arrow_y_values = [], [], []
    flag_base, flag_arrow = False, False

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
        print(f"Number of lines read: {len(lines)}")
        for line in lines:
            if line.startswith(base_str):
                flag_base = True
                flag_arrow = False
            if line.startswith(arrow_str):
                flag_base = False
                flag_arrow = True
            if line.strip() and not line.startswith('#'):
                try:
                    t, x, y = map(float, line.split())
                    if flag_base:
                        # print('base, time, position x, position y:', t, x, y)
                        time_base_ms.append(t)
                        base_x_values.append(x)
                        base_y_values.append(y)
                    if flag_arrow:
                        # print('arrow, time, position x, position y:', t, x, y)
                        time_arrow_ms.append(t)
                        arrow_x_values.append(x)
                        arrow_y_values.append(y)
                except ValueError:
                    # Skip lines that cannot be converted to float (e.g., headers)
                    pass

        # Offset time to zero
        time_base_ms = np.array(time_base_ms) - time_base_ms[0]
        time_arrow_ms = np.array(time_arrow_ms) - time_arrow_ms[0]

        pos_base = (time_base_ms, base_x_values, base_y_values)
        pos_arrow = (time_arrow_ms, arrow_x_values, arrow_y_values)

    return pos_base, pos_arrow


def plot_point_trajectory(file_path):
    time, x_values, y_values = read_point_trajectory_data(file_path)
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, label='Position', marker='o')
    # plt.plot(time,y_values, label='X Values', marker='o')
    # plt.plot(time, y_values, label='Y Values', marker='o')
    plt.xlabel('x value')
    plt.ylabel('y values')
    plt.title('Trajectory')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_arrow_trajectory(arrow_path, base_str: str, arrow_str: str):
    pos_base, pos_arrow = read_arrow_trajectory_data(
        arrow_path, base_str, arrow_str)

    time_base_ms, base_x_values, base_y_values = pos_base
    time_arrow_ms, arrow_x_values, arrow_y_values = pos_arrow

    frame_delay_ms = time_base_ms[1] - \
        time_base_ms[0]  # frame delay is about 33 ms

    skip_100ms = int(100/frame_delay_ms)
    skip_1s = int(1000/frame_delay_ms)
    skip = skip_1s

    plt.figure(figsize=(10, 6))
    plt.scatter(base_x_values[::skip], base_y_values[::skip],
                label='', marker='o', color='b')

    plt.plot(arrow_x_values[::skip], arrow_y_values[::skip],
             label='Tip Trajectory', marker='o', color='r')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Trajectory')
    plt.axis('equal')
    plt.legend()
    plt.grid(True)

    for i in range(0, len(arrow_x_values), skip):  # arrow every 100 ms
        # for i in range(0, len(time_base_ms), 30):  # arrow every 1000 ms
        try:
            # Compute the unit vector
            x_1, y_1 = (base_x_values[i], base_y_values[i])
            x_2, y_2 = (arrow_x_values[i], arrow_y_values[i])

            delta_x = abs(x_2-x_1)
            delta_y = abs(y_2-y_1)

            magnitude = math.sqrt(delta_x**2 + delta_y**2)
            d_x, d_y = (delta_x / magnitude) + \
                arrow_x_values[i], (delta_y / magnitude)+arrow_y_values[i]

            # Compute angle of rotation
            radian = math.atan2(delta_y, delta_x)
            angle = math.degrees((np.pi/2)-radian)
            str_angle = f'{angle:.1f}°'

            # Plot arrow and angles
            arrow_properties = dict(
                arrowstyle='->', color='b')  # Arrow properties
            plt.annotate(str_angle,
                         xy=(x_2, y_2), xytext=(x_1, y_1),
                         ha="center", va="center",
                         bbox=dict(boxstyle="round", fc="w"),
                         arrowprops=arrow_properties)

            # Add Color bar
            # Example color values, replace with the actual values
            color_values = [1, 2]
            sc = plt.scatter(
                x_2, y_2, c=color_values[i], cmap='viridis', label='Curvature []', alpha=0.7)

        except IndexError:
            print(f"Index {i} is out of range for the coordinate lists.")
            pass

    cbar = plt.colorbar(sc, label="Curvature [K] ")
    plt.show()


if __name__ == "__main__":
    # point_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Actuator\Single_Actuator_Media\Flexures\working_flexure2_rotation_circle_position\working_flexure2.txt"
    # plot_point_trajectory(point_path)
    # arrow_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Actuator\Single_Actuator_Media\Flexures\rupture_flexure_arrow_positions\underwater_failure_tube_v.txt"
    arrow_path = r"Actuator/Single_Actuator_Media/Flexures/rupture_flexure_arrow_positions/underwater_failure_tube_v.txt"
    plot_arrow_trajectory(arrow_path, '# pos_blue', '# pos_red')
