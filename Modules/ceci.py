# Import the required libraries
import customtkinter
import tkinterdnd2 as tkinterDnD
from tkinter import filedialog
import time
import os

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1400x780")
app.title("Combined Environment Control Interface")
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

radiobutton_var = customtkinter.IntVar(value=1)
label_font = ("Arial", 14)
desktop_directory = os.path.expanduser("~/Desktop")

frames = []
for i in range(4):
    frame = customtkinter.CTkFrame(master=app)
    frame.grid(row=0, column=i, padx=20, pady=20, sticky="nsew")
    frames.append(frame)

bottom_frame = customtkinter.CTkFrame(master=app)
bottom_frame.grid(row=1, column=0, columnspan=4,
                  padx=20, pady=20, sticky="nsew")


class Widget():
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory.set(directory)

    def start(self):
        print('Switch Syringe Pump: ', self.switch_1.get())
        print('Syringe Pump COM: ', self.combobox_1_0.get())
        print('Syringe Pump Syringe: ', self.segmented_button_1.get())
        print('Syringe Pump Syringe Type: ', self.combobox_1_2.get())
        print('Syringe Pump Syringe Volume: ', self.entry_1.get())
        print('Syringe Pump Flow Rate: ', self.entry_1_2.get())

        print('Switch Saleae: ', self.switch_2.get())
        print('Saleae COM: ', self.combobox_2.get())
        print('Saleae Channels: ', self.segmented_button_2.get())
        print('Saleae Buffer Size: ', self.combobox_2_1.get())
        print('Saleae Sampling Rate: ', self.combobox_2_2.get())
        print('Saleae Device Id: ', self.entry_2.get())

        print('Switch Fluigent: ', self.switch_3.get())

        print('Switch SLS: ', self.switch_4.get())

        print('Experiment Folder Name: ', self.entry_5_1.get())
        print('Export Directory: ', self.selected_directory.get())
        print('Capture Duration: ', self.entry_5.get())
        # duration = int(self.entry_5.get())

        # if duration > 0:
        #     self.countdown(duration)
        #     self.time_remaining.set(0)
        #     self.progressbar_5.set(0)

    def switch_syringe_pump(self):
        # Define logic for Syringe Pump switch
        pass

    def switch_saleae(self):
        # Define logic for Saleae switch
        pass

    def switch_fluigent(self):
        # Define logic for Fluigent switch
        pass

    def switch_sls(self):
        # Define logic for SLS switch
        pass

    def check_calibration(self):
        # Define logic for calibration checkbox
        pass

    switch_1 = customtkinter.CTkSwitch(
        master=frames[0], text="On/Off", command=switch_syringe_pump)
    combobox_1_0 = customtkinter.CTkComboBox(
        frames[0], values=[str(i) for i in range(1, 13)], width=200)
    segmented_button_1 = customtkinter.CTkSegmentedButton(
        master=frames[0], values=["       Syringe A       ", "       Syringe B       "], width=200)
    combobox_1_2 = customtkinter.CTkComboBox(
        frames[0], values=["BDP", "BDG"], width=200)
    entry_1 = customtkinter.CTkEntry(
        master=frames[0], placeholder_text="Syringe Volume [mL] ", width=200)
    entry_1_2 = customtkinter.CTkEntry(
        master=frames[0], placeholder_text="Flow Rate [uL/min] ", width=200)

    switch_2 = customtkinter.CTkSwitch(
        master=frames[1], text="On/Off", command=switch_saleae)
    checkbox_2 = customtkinter.CTkCheckBox(
        master=frames[1], text="Calibration", command=check_calibration)
    combobox_2 = customtkinter.CTkComboBox(
        frames[1], values=[str(i) for i in range(1, 13)], width=200)
    segmented_button_2 = customtkinter.CTkSegmentedButton(
        master=frames[1], values=[" Channel 0-1-2-3 ", " Channel 4-5-6-7 "], width=200)
    combobox_2_1 = customtkinter.CTkComboBox(
        frames[1],  values=[f"{i} GB" for i in range(1, 13)], width=200)
    combobox_2_2 = customtkinter.CTkComboBox(
        frames[1], values=['781250', '1562500', '3125000'], width=200)
    entry_2 = customtkinter.CTkEntry(
        master=frames[1], placeholder_text="Device Id", width=200)

    switch_3 = customtkinter.CTkSwitch(
        master=frames[2], text="On/Off", command=switch_fluigent)
    switch_4 = customtkinter.CTkSwitch(
        master=frames[3], text="On/Off", command=switch_sls)

    entry_5_1 = customtkinter.CTkEntry(
        master=bottom_frame, placeholder_text="Experiment Folder Name", width=400)
    select_location_button = customtkinter.CTkButton(
        master=bottom_frame, text="Change Export Directory", command=browse_directory)
    selected_directory = customtkinter.StringVar()
    selected_directory.set(desktop_directory)
    selected_directory_label = customtkinter.CTkLabel(
        master=bottom_frame, textvariable=selected_directory)
    entry_5 = customtkinter.CTkEntry(
        master=bottom_frame, placeholder_text="Capture Duration [s]", width=400)
    time_remaining = customtkinter.IntVar()
    time_remaining.set(0)
    time_remaining_label = customtkinter.CTkLabel(
        master=bottom_frame, textvariable=time_remaining, font=("Arial", 14))
    progressbar_5 = customtkinter.CTkProgressBar(
        master=bottom_frame, width=400, height=20, fg_color="#333333")
    progressbar_5.set(1)
    start_button = customtkinter.CTkButton(
        master=bottom_frame, text="Start", command=start)

    def countdown(self, duration):
        for i in range(duration, -1, -1):
            self.time_remaining.set(i)
            progress = 1 - ((duration - i) / duration)
            self.progressbar_5.set(progress)
            app.update()
            time.sleep(1)

    def create_syringe_pump_frame(self, app, width_syringe_frame=200):
        width_syringe_frame = width_syringe_frame

        self.frame_1 = customtkinter.CTkFrame(master=app)
        self.frame_1.grid(row=0, column=0, padx=60, pady=20, sticky="nsew")

        label_1 = customtkinter.CTkLabel(
            master=self.frame_1, justify=customtkinter.LEFT, text="SYRINGE PUMP", font=label_font)
        label_1.pack(pady=10, padx=10)

        self.switch_1 = customtkinter.CTkSwitch(
            master=self.frame_1, text="On/Off", command=self.switch_syringe_pump)
        self.switch_1.pack(pady=10, padx=10)

        self.combobox_1_0 = customtkinter.CTkComboBox(
            self.frame_1, values=[str(i) for i in range(1, 13)], width=width_syringe_frame)
        self.combobox_1_0.pack(pady=10, padx=10)
        self.combobox_1_0.set("Choose COM")

        self.segmented_button_1 = customtkinter.CTkSegmentedButton(
            master=self.frame_1, values=["       Syringe A       ", "       Syringe B       "], width=width_syringe_frame)
        self.segmented_button_1.pack(pady=10, padx=10)

        self.combobox_1_2 = customtkinter.CTkComboBox(
            self.frame_1, values=["BDP", "BDG"], width=width_syringe_frame)
        self.combobox_1_2.pack(pady=10, padx=10)
        self.combobox_1_2.set("Syringe Type")

        self.entry_1_text_var = customtkinter.StringVar()
        self.entry_1 = customtkinter.CTkEntry(
            master=self.frame_1, placeholder_text="Syringe Volume [mL] ", width=width_syringe_frame)
        self.entry_1.pack(pady=10, padx=10)

        self.entry_1_2 = customtkinter.CTkEntry(
            master=self.frame_1, placeholder_text="Flow Rate [uL/min] ", width=width_syringe_frame)
        self.entry_1_2.pack(pady=10, padx=10)

    def create_saleae_frame(self, app, width_saleae_frame=220):
        width_saleae = width_saleae_frame
        frame_2 = customtkinter.CTkFrame(master=app)
        frame_2.grid(row=0, column=1, padx=60, pady=20, sticky="nsew")

        label_2 = customtkinter.CTkLabel(
            master=frame_2, justify=customtkinter.LEFT, text="SALEAE", font=label_font)
        label_2.pack(pady=10, padx=10)

        self.switch_2 = customtkinter.CTkSwitch(
            master=frame_2, text="On/Off", command=self.switch_saleae)
        self.switch_2.pack(pady=10, padx=10)

        checkbox_2 = customtkinter.CTkCheckBox(
            master=frame_2, text="Calibration", command=self.check_calibration)
        checkbox_2.pack(pady=10, padx=10)

        self.combobox_2 = customtkinter.CTkComboBox(
            frame_2, values=[str(i) for i in range(1, 13)], width=width_saleae)
        self.combobox_2.pack(pady=10, padx=10)
        self.combobox_2.set("Choose COM")

        self.segmented_button_2 = customtkinter.CTkSegmentedButton(
            master=frame_2, values=[" Channel 0-1-2-3 ", " Channel 4-5-6-7 "], width=width_saleae)
        self.segmented_button_2.pack(pady=10, padx=10)

        self.combobox_2_1 = customtkinter.CTkComboBox(
            frame_2,  values=[f"{i} GB" for i in range(1, 13)], width=width_saleae)
        self.combobox_2_1.pack(pady=10, padx=10)
        self.combobox_2_1.set("Buffer Size [GB]")

        self.combobox_2_2 = customtkinter.CTkComboBox(
            frame_2, values=['781250', '1562500', '3125000'], width=width_saleae)
        self.combobox_2_2.pack(pady=10, padx=10)

        entry_2_text_var = customtkinter.StringVar()
        self.entry_2 = customtkinter.CTkEntry(
            master=frame_2, placeholder_text="Device Id", width=width_saleae)
        self.entry_2.pack(pady=10, padx=10)

    def create_fluigent_frame(self, app):
        self.frame_3 = customtkinter.CTkFrame(master=app)
        self.frame_3.grid(row=0, column=2, padx=60, pady=20, sticky="nsew")

        label_fluigent = customtkinter.CTkLabel(
            master=self.frame_3, justify=customtkinter.LEFT, text="FLUIGENT", font=label_font)
        label_fluigent.pack(pady=10, padx=10)

        self.switch_3 = customtkinter.CTkSwitch(
            master=self.frame_3, text="On/Off", command=self.switch_fluigent)
        self.switch_3.pack(pady=10, padx=10)

    def create_sls_frame(self, app):
        frame_4 = customtkinter.CTkFrame(master=app)
        frame_4.grid(row=0, column=3, padx=60, pady=20, sticky="nsew")

        label_sls = customtkinter.CTkLabel(
            master=frame_4, justify=customtkinter.LEFT, text="SLS", font=label_font)
        label_sls.pack(pady=10, padx=10)

        self.switch_4 = customtkinter.CTkSwitch(
            master=frame_4, text="On/Off", command=self.switch_sls)
        self.switch_4.pack(pady=10, padx=10)

    def create_capture_param_frame(self, app):
        frame_bottom = customtkinter.CTkFrame(master=app)
        frame_bottom.grid(row=1, column=0, columnspan=4, padx=10,
                          pady=10, sticky="nsew")

        label_5 = customtkinter.CTkLabel(
            master=frame_bottom, justify=customtkinter.LEFT, text="CAPTURE PARAMETERS", font=label_font)
        label_5.pack(pady=10, padx=10)

        width_bottom = 400

        self.entry_5_1 = customtkinter.CTkEntry(
            master=frame_bottom, placeholder_text="Experiment Folder Name", width=width_bottom)
        self.entry_5_1.pack(pady=10, padx=10)

        self.selected_directory = customtkinter.StringVar()
        self.selected_directory.set(desktop_directory)

        self.select_location_button = customtkinter.CTkButton(
            master=frame_bottom, text="Change Export Directory", command=self.browse_directory)
        self.select_location_button.pack(pady=10, padx=10)

        self.selected_directory_label = customtkinter.CTkLabel(
            master=frame_bottom, textvariable=self.selected_directory)
        self.selected_directory_label.pack(pady=10, padx=10)

        self.entry_5 = customtkinter.CTkEntry(
            master=frame_bottom, placeholder_text="Capture Duration [s]", width=width_bottom,)
        self.entry_5.pack(pady=10, padx=10)

        self.time_remaining = customtkinter.IntVar()
        self.time_remaining.set(0)
        self.time_remaining_label = customtkinter.CTkLabel(
            master=frame_bottom, textvariable=self.time_remaining, font=("Arial", 14))
        self.time_remaining_label.pack(pady=10, padx=10)

        self.progressbar_5 = customtkinter.CTkProgressBar(
            master=frame_bottom, width=width_bottom, height=20, fg_color="#333333")
        self.progressbar_5.pack(pady=2, padx=10)
        self.progressbar_5.set(1)

        self.start_button = customtkinter.CTkButton(
            master=frame_bottom, text="Start", command=self.start)
        self.start_button.pack(pady=10, padx=10)


for i in range(4):
    app.grid_columnconfigure(i, weight=1)

create_window = Widget()
create_window.create_syringe_pump_frame(app)
create_window.create_saleae_frame(app)
create_window.create_fluigent_frame(app)
create_window.create_sls_frame(app)
create_window.create_capture_param_frame(app)

app.mainloop()
