import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


def extract_data_from_xml(xml_data):
    root = ET.fromstring(xml_data)
    x_values = []
    y_values = []

    # Find all the rows in the first section (Table with header cells)
    # The first section starts with a row containing "Coords (x,y:cm; t:time)"
    start_row_found = False
    for row_number, row in enumerate(root.findall('.//Row')):
        if not start_row_found:
            # Check if this row contains the header "Coords (x,y:cm; t:time)"
            header_cell = row.find(
                './/Cell//Data[@ss:Type="String" and contains(., "Coords (x,y:cm; t:time)")]')
            if header_cell is not None:
                start_row_found = True
        else:
            # Extract x, y, and t values from the data cells
            cells = row.findall('Cell')
            if len(cells) == 3:
                x = float(cells[0].find('Data').text)
                y = float(cells[1].find('Data').text)

                # Append the values to their respective lists
                x_values.append(x)
                y_values.append(y)

    return x_values, y_values


def read_xml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def plot_trajectory(file_path):
    x_values, y_values = extract_data_from_xml(file_path)
    # Use row number as an approximate time index
    time = list(range(len(x_values)))
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
    xml_file_path = r"Actuator/Single_Actuator_Media/Flexures/working_flexure1_rotation_circle_position/working_flexure1_rotation_circle_position.xml"
    xml_data = read_xml_file(xml_file_path)
    plot_trajectory(xml_data)
