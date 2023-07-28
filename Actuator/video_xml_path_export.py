import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

def plot_xml_data(xml_file_path):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Find the relevant data within the XML structure
        data = []
        for track in root.findall(".//Track"):
            for coords in track.findall(".//Coords"):
                x = float(coords.get("x"))
                y = float(coords.get("y"))
                t = float(coords.get("t"))
                data.append((x, y, t))

        # Convert data to a Pandas DataFrame
        df = pd.DataFrame(data, columns=["x", "y", "t"])

        # Plot the data using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(df["x"], label="x")
        plt.plot(df["y"], label="y")
        plt.plot(df["t"], label="t")

        # Set plot title and labels
        plt.title("XML Data Plot")
        plt.xlabel("Index")
        plt.ylabel("Values")

        # Show the legend
        plt.legend()

        # Show the plot
        plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{xml_file_path}' was not found.")
    except Exception as e:
        print(f"Error: An error occurred while plotting the data.\n{e}")

if __name__ == "__main__":
    # Replace 'your_file.xml' with the path to your XML file
    file_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Actuator\Single_Actuator_Video\Flexures\working_flexure1_rotation_circle_position\working_flexure1_rotation_circle_position.xml"
    plot_xml_data(file_path)
