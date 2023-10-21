# Import the required libraries
import customtkinter
import tkinterdnd2 as tkinterDnD
from tkinter import filedialog  # Import filedialog from tkinter
import time
import os

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1400x780")
app.title("Combined Environment Control Interface")

# Create a list to store the frames
frames = []
radiobutton_var = customtkinter.IntVar(value=1)
label_font = ("Arial", 14)  # Change the font family and size as needed
# Determine the desktop directory path based on the user's platform
desktop_directory = os.path.expanduser("~/Desktop")


def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        selected_directory.set(directory)


# Create a countdown function
def countdown(duration):
    for i in range(duration, -1, -1):
        time_remaining.set(i)  # Update the time remaining
        # Calculate progress percentage
        progress = 1 - ((duration - i) / duration)
        progressbar_5.set(progress)  # Update the progress bar
        app.update()  # Update the tkinter GUI
        time.sleep(0.5)  # Wait for 1 second


# Create a Start Countdown button callback
def start():
    print('Switch Syringe Pump: ', switch_1.get())
    print('Syringe Pump COM: ', combobox_1_0.get())
    print('Syringe Pump Syringe: ', segmented_button_1.get())
    print('Syringe Pump Syringe Type: ', combobox_1_2.get())
    print('Syringe Pump Syringe Volume: ', entry_1.get())
    print('Syringe Pump Flow Rate: ', entry_1_2.get())

    print('Switch Saleae: ', switch_2.get())
    print('Saleae COM: ', combobox_2.get())
    print('Saleae Channels: ', segmented_button_2.get())
    print('Saleae Buffer Size: ', combobox_2_1.get())
    print('Saleae Sampling Rate: ', combobox_2_2.get())
    print('Saleae Device Id: ', entry_2.get())
    print('Saleae Flow Rate: ', entry_2_2.get())

    print('Switch Fluigent: ', switch_3.get())
    # print('Fluigent Number of Controllers: ', combobox_fluigent.get())

    print('Switch SLS: ', switch_4.get())

    print('Experiment Folder Name: ', entry_5_1.get())
    print('Export Directory: ', selected_directory.get())
    print('Capture Duration: ', entry_5.get())
    duration = int(entry_5.get())

    if duration > 0:
        countdown(duration)
        time_remaining.set(0)
        progressbar_5.set(0)


# Create four frames in a row
for i in range(4):
    frame = customtkinter.CTkFrame(master=app)
    frame.grid(row=0, column=i, padx=20, pady=20, sticky="nsew")
    frames.append(frame)

# Create the bottom frame that spans all four columns
bottom_frame = customtkinter.CTkFrame(master=app)
bottom_frame.grid(row=1, column=0, columnspan=4,
                  padx=20, pady=20, sticky="nsew")


def button_callback():
    print("Button click")


#############################################################
# SYRINGE PUMP
#############################################################

width_syringe = 220

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.grid(row=0, column=0, padx=60, pady=20, sticky="nsew")

label_1 = customtkinter.CTkLabel(
    master=frame_1, justify=customtkinter.LEFT, text="SYRINGE PUMP", font=label_font)
label_1.pack(pady=10, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1, text="On/Off")
switch_1.pack(pady=10, padx=10)

combobox_1_0 = customtkinter.CTkComboBox(
    frame_1, values=[str(i) for i in range(1, 13)], width=width_syringe)
combobox_1_0.pack(pady=10, padx=10)
combobox_1_0.set("Choose COM")

# Set the width of the segmented button to match the combobox
segmented_button_1 = customtkinter.CTkSegmentedButton(
    master=frame_1, values=["       Syringe A       ", "       Syringe B       "], width=width_syringe)
segmented_button_1.pack(pady=10, padx=10)

combobox_1_2 = customtkinter.CTkComboBox(
    frame_1, values=["BDP", "BDG"], width=width_syringe)
combobox_1_2.pack(pady=10, padx=10)
combobox_1_2.set("Syringe Type")

entry_1_text_var = customtkinter.StringVar()
entry_1 = customtkinter.CTkEntry(
    master=frame_1, placeholder_text="Syringe Volume [mL] ", width=width_syringe)
entry_1.pack(pady=10, padx=10)

entry_1_2 = customtkinter.CTkEntry(
    master=frame_1, placeholder_text="Flow Rate [uL/min] ", width=width_syringe)
entry_1_2.pack(pady=10, padx=10)

#############################################################
# SALEAE
#############################################################

width_saleae = 220
frame_2 = customtkinter.CTkFrame(master=app)
frame_2.grid(row=0, column=1, padx=60, pady=20, sticky="nsew")

label_2 = customtkinter.CTkLabel(
    master=frame_2, justify=customtkinter.LEFT, text="SALEAE", font=label_font)
label_2.pack(pady=10, padx=10)

switch_2 = customtkinter.CTkSwitch(master=frame_2, text="On/Off")
switch_2.pack(pady=10, padx=10)

combobox_2 = customtkinter.CTkComboBox(
    frame_2, values=[str(i) for i in range(1, 13)], width=width_saleae)
combobox_2.pack(pady=10, padx=10)
combobox_2.set("Choose COM")

segmented_button_2 = customtkinter.CTkSegmentedButton(
    master=frame_2, values=[" Channel 0-1-2-3 ", " Channel 4-5-6-7 "], width=width_syringe)
segmented_button_2.pack(pady=10, padx=10)

combobox_2_1 = customtkinter.CTkComboBox(
    frame_2,  values=[f"{i} GB" for i in range(1, 13)], width=width_saleae)
combobox_2_1.pack(pady=10, padx=10)
combobox_2_1.set("Buffer Size [GB]")

combobox_2_2 = customtkinter.CTkComboBox(
    frame_2, values=['781250', '1562500', '3125000'], width=width_saleae)
combobox_2_2.pack(pady=10, padx=10)
combobox_2_2.set("Sampling Rate [Samples/second]")

entry_2_text_var = customtkinter.StringVar()
entry_2 = customtkinter.CTkEntry(
    master=frame_2, placeholder_text="Device Id", width=width_saleae)
entry_2.pack(pady=10, padx=10)

entry_2_2 = customtkinter.CTkEntry(
    master=frame_2, placeholder_text="Flow Rate [uL/min] ", width=width_saleae)
entry_2_2.pack(pady=10, padx=10)


#############################################################
# FLUIGENT
#############################################################
frame_3 = customtkinter.CTkFrame(master=app)
frame_3.grid(row=0, column=2, padx=60, pady=20, sticky="nsew")

label_fluigent = customtkinter.CTkLabel(
    master=frame_3, justify=customtkinter.LEFT, text="FLUIGENT", font=label_font)
label_fluigent.pack(pady=10, padx=10)

switch_3 = customtkinter.CTkSwitch(master=frame_3, text="On/Off")
switch_3.pack(pady=10, padx=10)

# # Combobox to select the number of pressure controllers
# combobox_fluigent = customtkinter.CTkComboBox(
#     frame_3, values=["1 Controller", "2 Controllers"])
# combobox_fluigent.pack(pady=10, padx=10)
# combobox_fluigent.set("Select Number of Controllers")

#############################################################
# SLS
#############################################################
frame_4 = customtkinter.CTkFrame(master=app)
frame_4.grid(row=0, column=3, padx=60, pady=20, sticky="nsew")

label_sls = customtkinter.CTkLabel(
    master=frame_4, justify=customtkinter.LEFT, text="SLS", font=label_font)
label_sls.pack(pady=10, padx=10)

switch_4 = customtkinter.CTkSwitch(master=frame_4, text="On/Off")
switch_4.pack(pady=10, padx=10)

#############################################################
# CAPTURE PARAMETERS
#############################################################
frame_bottom = customtkinter.CTkFrame(master=app)
frame_bottom.grid(row=1, column=0, columnspan=4, padx=10,
                  pady=10, sticky="nsew")  # Use grid

label_5 = customtkinter.CTkLabel(
    master=frame_bottom, justify=customtkinter.LEFT, text="CAPTURE PARAMETERS", font=label_font)
label_5.pack(pady=10, padx=10)

width_bottom = 400

entry_5_1 = customtkinter.CTkEntry(
    master=frame_bottom, placeholder_text="Experiment Folder Name", width=width_bottom)
entry_5_1.pack(pady=10, padx=10)

# Select desktop as default save directory
selected_directory = customtkinter.StringVar()
# Set the initial directory to the desktop
selected_directory.set(desktop_directory)

select_location_button = customtkinter.CTkButton(
    master=frame_bottom, text="Change Export Directory", command=browse_directory)
select_location_button.pack(pady=10, padx=10)

selected_directory_label = customtkinter.CTkLabel(
    master=frame_bottom, textvariable=selected_directory)
selected_directory_label.pack(pady=10, padx=10)

entry_5 = customtkinter.CTkEntry(
    master=frame_bottom, placeholder_text="Capture Duration [s]", width=width_bottom,)
entry_5.pack(pady=10, padx=10)

# Create a label to display the time remaining
time_remaining = customtkinter.IntVar()
time_remaining.set(0)
time_remaining_label = customtkinter.CTkLabel(
    master=frame_bottom, textvariable=time_remaining, font=("Arial", 14))
time_remaining_label.pack(pady=10, padx=10)

# Create a progress bar
progressbar_5 = customtkinter.CTkProgressBar(
    master=frame_bottom, width=width_bottom, height=20, fg_color="#333333")
progressbar_5.pack(pady=2, padx=10)
progressbar_5.set(1)

# Create a Start Countdown button
start_button = customtkinter.CTkButton(
    master=frame_bottom, text="Start", command=start)
start_button.pack(pady=10, padx=10)


button_5 = customtkinter.CTkButton(
    master=frame_bottom, text="START", command=button_callback)
button_5.pack(pady=10, padx=10)

# Add your additional code here

app.mainloop()
