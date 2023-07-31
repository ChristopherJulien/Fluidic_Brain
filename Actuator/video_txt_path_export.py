import matplotlib.pyplot as plt
import numpy as np

def read_trajectory_data(file_path):
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
                    if y >2:
                        x_values.append(-x)
                        y_values.append(y)
                except ValueError:
                    # Skip lines that cannot be converted to float (e.g., headers)
                    pass

    return time, x_values, y_values


def plot_trajectory(file_path):
    time, x_values, y_values = read_trajectory_data(file_path)
    plt.figure(figsize=(10, 6))
    plt.plot(x_values,y_values, label='Position', marker='o')
    # plt.plot(time,y_values, label='X Values', marker='o')
    # plt.plot(time, y_values, label='Y Values', marker='o')
    plt.xlabel('x value')
    plt.ylabel('y values')
    plt.title('Trajectory')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    file_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Actuator\Single_Actuator_Media\Flexures\working_flexure2_rotation_circle_position\working_flexure2.txt"
    plot_trajectory(file_path)
