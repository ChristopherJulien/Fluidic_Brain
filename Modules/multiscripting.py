import subprocess

# Replace these with the paths to your three Python scripts
script1_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\SLS_1500.py"
script2_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Saleae.py"
script3_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Push_Pull_Pressure.py"

# Define a function to run the scripts
def run_script(script_path):
    process = subprocess.Popen(["python", script_path])
    return process

def close_script(process):
    process.communicate()
    process.kill()    

# Start each script in a separate process
process3 = run_script(script3_path)
process1 = run_script(script1_path)
process2 = run_script(script2_path)

close_script(process3)
close_script(process1)
close_script(process2)
