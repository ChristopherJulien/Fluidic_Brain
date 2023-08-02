import matplotlib.pyplot as plt
import numpy as np


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
    time_base, base_x_values, base_y_values = [], [], []
    time_arrow, arrow_x_values, arrow_y_values = [], [], []
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
                        print('base, time, position x, position y:', t, x, y)
                        time_base.append(t)
                        base_x_values.append(x)
                        base_y_values.append(y)
                    if flag_arrow:
                        print('arrow, time, position x, position y:', t, x, y)
                        time_arrow.append(t)
                        arrow_x_values.append(x)
                        arrow_y_values.append(y)
                except ValueError:
                    # Skip lines that cannot be converted to float (e.g., headers)
                    pass

        pos_base = (time_base, base_x_values, base_y_values)
        pos_arrow = (time_arrow, arrow_x_values, arrow_y_values)

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


def plot_arrow_trajectory(fiLe_path, base_str: str, arrow_str: str):
    pose_base, pose_arrow = read_arrow_trajectory_data(
        arrow_path, base_str, arrow_str)

    time_base, base_x_values, base_y_values = pose_base
    time_arrow, arrow_x_values, arrow_y_values = pose_arrow

    plt.figure(figsize=(10, 6))
    plt.plot(base_x_values, base_y_values, label='Base', marker='o', color='b')
    plt.plot(arrow_x_values, arrow_y_values,
             label='Arrow', marker='o', color='r')

    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Trajectory')
    plt.legend()
    plt.grid(True)

    # Adding arrows between the base and arrow points
    for i in range(len(base_x_values)):
        # Base point coordinates
        arrow_base_point = (base_x_values[i], base_y_values[i])
        # Arrow point coordinates
        arrow_end_point = (arrow_x_values[i], arrow_y_values[i])
        arrow_properties = dict(arrowstyle='->', color='b')  # Arrow properties

        plt.annotate('', xy=arrow_end_point, xytext=arrow_base_point,
                     arrowprops=arrow_properties)

    plt.show()


if __name__ == "__main__":
    # point_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Actuator\Single_Actuator_Media\Flexures\working_flexure2_rotation_circle_position\working_flexure2.txt"
    # plot_point_trajectory(point_path)
    arrow_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Actuator\Single_Actuator_Media\Failure\underwater_failure_tube_v\underwater_failure_tube_v.txt"
    plot_arrow_trajectory(arrow_path, '# pos_blue', '# pos_red')
