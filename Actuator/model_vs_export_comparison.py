import matplotlib.pyplot as plt
import numpy as np
import math
import sys

Length = 4.73  # cm
Width = 0.24  # cm
angles = np.linspace(-75*(np.pi)/180, 67*(np.pi) /
                     180, 1000)  # Generate x values

x_offset = 0.0  # cm
y_offset = 0.0  # cm


def get_pos_video(file_path):
    time = []
    x_values = []
    y_values = []
    x_video_offset = 0.0  # cm'
    y_video_offset = 0.0  # cm

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
        print(f"Number of lines read: {len(lines)}")
        for line in lines:
            if line.strip() and not line.startswith('#'):
                try:
                    t, x, y = map(float, line.split())
                    # print('time, position x, position y:', t, x, y)
                    time.append(t)
                    x_values.append(-x + x_video_offset)
                    y_values.append(y + y_video_offset)
                except ValueError:
                    # Skip lines that cannot be converted to float (e.g., headers)
                    pass

    return time, x_values, y_values


def get_pos_model_1(angle, L=Length, W=Width):
    R = L/2
    print('Model 1: R =', R)
    return R*np.cos(angle) + x_offset, R*np.sin(angle) + y_offset


def get_pos_model_2(angle, L=Length, W=Width):
    R = math.sqrt((L/2)**2 + W**2)
    print('Model 2: R =', R)
    return R*np.cos(angle) + x_offset, R*np.sin(angle) + y_offset


def get_pos_model_3(angle, L=Length, W=Width):
    R = math.sqrt((L/2)**2 + (1.5*W)**2)
    print('Model 3: R =', R)
    return R*np.cos(angle) + x_offset, R*np.sin(angle) + y_offset


def plot_trajectory_all_models(file_path, angles, L=Length, W=Width):
    file_path = file_path
    # Calculate the positions for the three models
    x1, y1 = get_pos_model_1(angles)
    x2, y2 = get_pos_model_2(angles)
    x3, y3 = get_pos_model_3(angles)
    _, x4, y4 = get_pos_video(file_path)

    # Create the plot with all three models superimposed
    plt.figure(figsize=(8, 6))
    plt.plot(x1, y1, label="Model 1 Trajectory")
    plt.plot(x2, y2, label="Model 2 Trajectory")
    plt.plot(x3, y3, label="Model 3 Trajectory")
    plt.plot(x4, y4, label="Video Trajectory")

    # Set labels and title
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Model Trajectories vs Video Trajectory")

    # Add a legend
    legend_text = "Actuator Length  {}cm".format(Length)
    plt.legend(title=legend_text)
    plt.show()


def plot_error_all_models():
    pass


if __name__ == "__main__":
    file_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Actuator\Single_Actuator_Media\Flexures\working_flexure2_rotation_circle_position\working_flexure2.txt"
    plot_trajectory_all_models(file_path, angles)

    _, experimental_x, experimental_y = get_pos_video(file_path)
    theoretical_x1, theoretical_y1 = get_pos_model_1(angles)
    theoretical_x2, theoretical_y2 = get_pos_model_2(angles)
    theoretical_x3, theoretical_y3 = get_pos_model_3(angles)

    # Create a common set of x-values to resample/interpolate both curves
    common_x1 = np.linspace(min(min(experimental_x), min(theoretical_x1)),
                            max(max(experimental_x), max(theoretical_x1)), 10000)
    print(common_x1)

    # common_x2 = np.linspace(min(min(experimental_x), min(theoretical_x2)),
    #                         max(max(experimental_x), max(theoretical_x2)), 100)
    # common_x3 = np.linspace(min(min(experimental_x), min(theoretical_x3)),
    # max(max(experimental_x), max(theoretical_x3)), 100)

    # Interpolate or resample both curves onto the common x-values
    experimental_interp_y1 = np.interp(
        common_x1, experimental_x, experimental_y)
    # experimental_interp_y2 = np.interp(common_x2, experimental_x, experimental_y)
    # experimental_interp_y3 = np.interp(common_x3, experimental_x, experimental_y)

    theoretical_interp_y1 = np.interp(
        common_x1, theoretical_x1, theoretical_y1)
    # theoretical_interp_y2 = np.interp(
    #     common_x2, theoretical_x2, theoretical_y2)
    # theoretical_interp_y3 = np.interp(
    #     common_x3, theoretical_x3, theoretical_y3)

    # # Calculate the error between the two interpolated curves

    error_1 = abs((experimental_interp_y1 - theoretical_interp_y1) * 100 /
                  experimental_interp_y1)
    # error_1 = abs(experimental_interp_y1 - theoretical_interp_y1) / \
    # (max(experimental_interp_y1) - min(experimental_interp_y1)) * 100
    # print('Error 1:', error_1)
    # error_2 = abs(experimental_interp_y2 - theoretical_interp_y2) / \
    #     (max(experimental_interp_y2) - min(experimental_interp_y2)) * 100
    # error_3 = abs(experimental_interp_y3 - theoretical_interp_y3) / \
    #     (max(experimental_interp_y3) - min(experimental_interp_y3)) * 100

    # # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(8, 6))
    # plt.errorbar(experimental_interp_y, q_measured_list, yerr=q_std_list, fmt='o', capsize=5, label='Measured')
    # plt.plot(q_set_list, q_set_list, label='Set', linestyle='--')
    # plt.plot(q_set_fit, q_measured_fit, color='red', label='Fitted Line  (Degree '+str(degree) + ')'

    # # Plot the error between the two curves
    ax.plot(common_x1, error_1, label='Error % Model 1')
    # ax.plot(common_x2, error_2, label='Error % Model 2')
    # ax.plot(common_x3, error_3, label='Error % Model 3')

    # # Set labels and title
    ax.set_xlabel("X-values")
    ax.set_ylabel("% Error")
    ax.set_title("Error between Experimental and Theoretical Curves")

    # # Add a legend
    ax.legend()
    plt.show()
