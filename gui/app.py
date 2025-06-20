import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import re
import json


def update_range_in_config(new_range):
    config_path = os.path.join(os.getcwd(), "settings", "config.json")

    try:
        # Load current config
        with open(config_path, "r") as f:
            config_data = json.load(f)

        # Update the value
        config_data["user.range"] = str(new_range)

        # Write back to file
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)

        print(f"✅ Config updated: user.range = {new_range}")

    except Exception as e:
        messagebox.showerror("Config Error", f"Failed to update range in config:\n{e}")

def clean_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class FlightRouteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Route Optimizer")

        # RANGE input
        tk.Label(root, text="Aircraft Range (nm):").grid(row=0, column=0, sticky="e")
        self.range_entry = tk.Entry(root)
        self.range_entry.grid(row=0, column=1)
        tk.Button(root, text="Set Range", command=self.run_range_step).grid(row=0, column=2, padx=5)

        # ICAO selection
        tk.Label(root, text="Source ICAO:").grid(row=1, column=0, sticky="e")
        self.source_entry = tk.Entry(root)
        self.source_entry.grid(row=1, column=1)

        tk.Label(root, text="Destination ICAO:").grid(row=2, column=0, sticky="e")
        self.dest_entry = tk.Entry(root)
        self.dest_entry.grid(row=2, column=1)

        tk.Button(root, text="Find Route", command=self.run_final_step).grid(row=2, column=2, padx=5)

        # Output Box
        self.output_box = tk.Text(root, height=25, width=80)
        self.output_box.grid(row=3, column=0, columnspan=3, pady=10)

        self.exe = os.path.join(os.getcwd(), "build", "flightPathOptimizer.exe") if os.name == "nt" else "./flightPathOptimizer"

        # Run fetch script immediately
        self.fetch_airport_data()

    def fetch_airport_data(self):
        try:
            script_path = os.path.join(os.getcwd(), "scripts", "fetchAirportData.py")
            subprocess.run([sys.executable, script_path], check=True)
            print("✅ Airport data refreshed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch airport data:\n{e}")

    def run_range_step(self):
        rng = self.range_entry.get().strip()
        if not rng.isdigit():
            messagebox.showerror("Input Error", "Please enter a valid numeric range.")
            return

        # Simulate input: always 'y' for fetch, then range, then 'exit' to break loop
        input_data = f"y\n{rng}\nexit\n"


        try:
            proc = subprocess.Popen(
                [self.exe],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(input=input_data)

            self.output_box.delete(1.0, tk.END)
            if stderr:
                self.output_box.insert(tk.END, f"[ERROR]:\n{stderr}\n")
            self.output_box.insert(tk.END, f"[ICAO Codes in Range {rng}nm]:\n{stdout}\n")
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))
            
        update_range_in_config(rng)

    def run_final_step(self):
        rng = self.range_entry.get().strip()
        start = self.source_entry.get().strip().upper()
        dest = self.dest_entry.get().strip().upper()

        if not (rng.isdigit() and start and dest):
            messagebox.showerror("Input Error", "Fill range and valid ICAO codes.")
            return

        # Simulate: always 'y' again, same range, then ICAO codes
        input_data = f"y\n{start}\n{dest}\n"

        try:
            proc = subprocess.Popen(
                [self.exe],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(input=input_data)

            self.output_box.insert(tk.END, f"\n\n[Shortest Route from {start} to {dest}]:\n")
            if stderr:
                self.output_box.insert(tk.END, f"[ERROR]:\n{stderr}\n")
                
            cleaned_output = clean_ansi(stdout)
            self.output_box.insert(tk.END, f"{cleaned_output}\n")

        except Exception as e:
            messagebox.showerror("Execution Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightRouteApp(root)
    root.mainloop()
