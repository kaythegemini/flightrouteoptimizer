"""
@file: app.py
@author: kaythegemini

Script to grab airport location data from OurAirports API
and convert it into a JSON file
"""

import os
import json
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess


valid_icaos = [
    "IN-0003", "IN-0010", "IN-0011", "IN-0012", "IN-0013", "IN-0015", "IN-0023", "IN-0024", "IN-0025", "IN-0026", "IN-0033", "IN-0034", "IN-0053", "IN-0060", "IN-0061", "IN-0062", "IN-0064", "IN-0065", "IN-0066", "IN-0067", "IN-0068", "IN-0069", "IN-0070", "IN-0072", "IN-0073", "IN-0074", "IN-0077", "IN-0085", "IN-0086", "IN-0087", "IN-0088", "IN-0089", "IN-0090", "IN-0091", "IN-0093", "IN-0096", "IN-0097", "IN-0099", "IN-0100", "IN-0101", "IN-0102", "IN-0106", "IN-0107", "IN-0176", "IN-0177", "IN-0279", "IN-0283", "IN-0300", "IN-0302", "IN-0307", "IN-0308", "IN-0338", "IN-0341", "IN-0342", "IN-0343", "IN-0345", "IN-0346", "IN-0360", "IN-JGB", "IN-NVY", "IN-RJI", "IN-TEI", "IN-VA38", "IN-VA47", "IN-VA51", "IN-VA53", "IN-VA74", "OMN", "VA1B", "VA1C", "VA1D", "VA1E", "VA1F", "VA1G", "VA1H", "VA1J", "VA1K", "VA1L", "VA1M", "VA1N", "VA1O", "VA1P", "VA2A", "VA2B", "VA2C", "VA2D", "VAAH", "VAAK", "VAAU", "VABB", "VABI", "VABJ", "VABM", "VABO", "VABP", "VABV", "VADN", "VADS", "VAGN", "VAGO", "VAHB", "VAID", "VAJB", "VAJJ", "VAJM", "VAKE", "VAKJ", "VAKP", "VAKS", "VAMA", "VAND", "VANP", "VAOZ", "VAPO", "VAPR", "VARG", "VARK", "VARP", "VASD", "VASL", "VASU", "VAUD", "VE23", "VE24", "VE36", "VE41", "VE44", "VE54", "VE62", "VE67", "VE85", "VE89", "VE91", "VE96", "VEAN", "VEAT", "VEAZ", "VEBA", "VEBD", "VEBG", "VEBI", "VEBK", "VEBM", "VEBS", "VECA", "VECC", "VECK", "VECO", "VEDB", "VEDG", "VEDX", "VEDZ", "VEGK", "VEGT", "VEGY", "VEHK", "VEIM", "VEJH", "VEJP", "VEJS", "VEJT", "VEKI", "VEKJ", "VEKM", "VEKR", "VEKU", "VEKW", "VELP", "VELR", "VEMH", "VEMN", "VEMR", "VEMZ", "VENP", "VEPG", "VEPH", "VEPI", "VEPT", "VEPU", "VERC", "VERK", "VERL", "VERU", "VETZ", "VEUK", "VEVZ", "VEZO", "VI00", "VI20", "VI40", "VI43", "VI57", "VI65", "VI66", "VI69", "VI70", "VI71", "VI73", "VI75", "VI76", "VI82", "VI88", "VI90", "VIAG", "VIAH", "VIAL", "VIAM", "VIAR", "VIAW", "VIAX", "VIBK", "VIBL", "VIBN", "VIBR", "VIBT", "VIBW", "VIBY", "VICG", "VICX", "VIDD", "VIDF", "VIDN", "VIDP", "VIDX", "VIGG", "VIGR", "VIHR", "VIHX", "VIJN", "VIJO", "VIJP", "VIJR", "VIJU", "VIKA", "VIKG", "VIKO", "VILD", "VILH", "VILK", "VILP", "VIPK", "VIPL", "VIPT", "VIRB", "VISA", "VISM", "VISP", "VISR", "VIST", "VIUT", "VIUX", "VO26", "VO52", "VO55", "VO80", "VO94", "VO95", "VOAR", "VOAT", "VOBG", "VOBI", "VOBL", "VOBR", "VOBZ", "VOCB", "VOCC", "VOCI", "VOCL", "VOCP", "VOCX", "VODG", "VOHK", "VOHS", "VOHY", "VOKN", "VOKP", "VOKU", "VOMD", "VOML", "VOMM", "VOMY", "VONS", "VOPB", "VOPC", "VOPN", "VORG", "VORM", "VORY", "VOSM", "VOSX", "VOTJ", "VOTP", "VOTR", "VOTV", "VOTX", "VOVR", "VOWA", "VOYK"
]


# Clean ANSI escape codes from terminal output
def clean_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


# Update config.json with new range
def update_range_in_config(new_range):
    config_path = os.path.join(os.getcwd(), "settings", "config.json")
    try:
        with open(config_path, "r") as f:
            config_data = json.load(f)
        config_data["user.range"] = str(new_range)
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        messagebox.showerror(
            "Config Error", f"Failed to update range in config:\n{e}")


class FlightRouteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Route Optimizer")
        self.root.geometry("1200x600")

        self.exe_path = os.path.join(
            os.getcwd(), "build", "flightPathOptimizer.exe")

        self.build_gui()

    def build_gui(self):
        # Main layout
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Left panel (controls)
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(control_frame, text="Set Aircraft Range (nm):").pack(
            anchor="w")
        self.range_entry = ttk.Entry(control_frame, width=25)
        self.range_entry.pack(anchor="w")

        self.set_range_button = ttk.Button(
            control_frame, text="Set Range", command=self.run_range_step)
        self.set_range_button.pack(pady=5)

        ttk.Separator(control_frame, orient="horizontal").pack(
            fill="x", pady=10)

        ttk.Label(control_frame, text="Source ICAO:").pack(anchor="w")
        self.source_entry = ttk.Entry(
            control_frame, width=25, state="disabled")
        self.source_entry.pack(anchor="w")

        ttk.Label(control_frame, text="Destination ICAO:").pack(anchor="w")
        self.dest_entry = ttk.Entry(control_frame, width=25, state="disabled")
        self.dest_entry.pack(anchor="w")

        self.find_button = ttk.Button(
            control_frame, text="Find Route", state="disabled", command=self.run_final_step)
        self.find_button.pack(pady=5)

        # Output box (center)
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(side="left", fill="both", expand=True)

        self.output_box = scrolledtext.ScrolledText(
            output_frame, wrap=tk.WORD, height=30, width=70)
        self.output_box.pack(fill="both", expand=True)

        # Right panel (ICAO List)
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side="right", fill="both", padx=10, pady=10)

        ttk.Label(right_panel, text="Available ICAO Codes:").pack(anchor="w")

        icao_text = tk.Text(right_panel, wrap="none", height=30, width=45)
        icao_text.pack(expand=True, fill="both")

        # Full list of ICAO codes

        # Display codes in left-to-right grid format with fixed spacing
        formatted_text = ""
        codes_per_line = 5  # you can adjust for tighter/wider layout
        for i, code in enumerate(valid_icaos):
            formatted_text += f"{code:<9}"  # left-align with 9-character width
            if (i + 1) % codes_per_line == 0:
                formatted_text += "\n"

        icao_text.insert(tk.END, formatted_text)
        icao_text.config(state="disabled", font=("Courier New", 10))

    def run_range_step(self):
        rng = self.range_entry.get().strip()
        if not rng.isdigit():
            messagebox.showerror(
                "Input Error", "Please enter a valid numeric range.")
            return

        update_range_in_config(rng)
        self.output_box.insert(
            tk.END, f"\nSetting range to {rng} nm and generating graph...\n")

        try:
            proc = subprocess.Popen(
                [self.exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(input="exit\n")
            cleaned = clean_ansi(stdout)
            self.output_box.insert(tk.END, cleaned + "\n")

            self.source_entry.config(state="normal")
            self.dest_entry.config(state="normal")
            self.find_button.config(state="normal")

            messagebox.showinfo(
                "Range Set", "Range updated and graph generated successfully.")
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def run_final_step(self):
        start = self.source_entry.get().strip().upper()
        dest = self.dest_entry.get().strip().upper()

        if not start or not dest:
            messagebox.showerror(
                "Input Error", "Please enter both ICAO codes.")
            return

        if start not in valid_icaos or dest not in valid_icaos:
            messagebox.showerror(
                "Invalid ICAO", "One or both ICAO codes are not in the list.")
            self.source_entry.delete(0, tk.END)
            self.dest_entry.delete(0, tk.END)
            return  # Do not run the binary if ICAO is invalid

        # Construct input and run binary only if ICAO codes are valid
        input_data = f"{start}\n{dest}\n"
        try:
            proc = subprocess.Popen(
                [self.exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(input=input_data)
            cleaned_output = clean_ansi(stdout)

            # Display output
            self.output_box.insert(
                tk.END, f"\n\n[Shortest Route from {start} to {dest}]:\n")
            if stderr:
                self.output_box.insert(tk.END, f"[ERROR]:\n{stderr}\n")
            self.output_box.insert(tk.END, f"{cleaned_output}\n")

        except Exception as e:
            messagebox.showerror("Execution Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightRouteGUI(root)
    root.mainloop()
