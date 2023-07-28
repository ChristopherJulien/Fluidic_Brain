import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def convert_time(time_str):
    # Convert time from the format "0.00" to float
    return float(time_str)

def read_trajectory_data(file_path):
    time = []
    x_values = []
    y_values = []

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the "Track" element (if it exists)
    track_element = root.find(".//Track")

    if track_element is not None:
        # Find the "Coords" elements within the "Track" element and extract the numeric values
        for coord in track_element.findall(".//Coords"):
            x, y, t = map(float, coord.text.split())
            time.append(convert_time(t))
            x_values.append(x)
            y_values.append(y)

    return time, x_values, y_values

def plot_trajectory(file_path):
    time, x_values, y_values = read_trajectory_data(file_path)
    plt.figure(figsize=(10, 6))
    plt.plot(time, x_values, label='X Values', marker='o')
    plt.plot(time, y_values, label='Y Values', marker='o')
    plt.xlabel('Time')
    plt.ylabel('X and Y Values')
    plt.title('X and Y Values vs. Time')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    xml_file_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Actuator\Single_Actuator_Video\Flexures\working_flexure1_rotation_circle_position\working_flexure1_rotation_circle_position.xml"
    plot_trajectory(xml_file_path)
