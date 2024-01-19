# Copyright (C) 2024 Theros <https://github.com/therosin>
#
# This file is part of SubnetPlanner.
#
# SubnetPlanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SubnetPlanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SubnetPlanner.  If not, see <http://www.gnu.org/licenses/>.

import tkinter as tk
from tkinter import ttk
import ipaddress
import math

cidr_entry = None
networks_entry = None
result_frame = None
status_label = None
canvas = None


def display_error(message):
    clear_results()
    update_status(
        f"Error: {message}", error=True
    )  # Update status bar with error message
    error_label = tk.Label(
        result_frame,
        text=message,
        borderwidth=2,
        relief="groove",
        fg="white",
        bg="red",
        wraplength=230,
    )
    error_label.pack(pady=3, fill="both", expand=True, anchor="w")
    # BUG reset scrollable area to top to ensure the frame gets updated correctly.
    canvas.yview_moveto(0)


def clear_results():
    for widget in result_frame.winfo_children():
        widget.destroy()


def update_status(message, error=False):
    status_label.config(text=message, fg="red" if error else "black")


def calculate_subnets():
    clear_results()
    try:
        cidr = cidr_entry.get()
        num_networks = int(networks_entry.get())
        network = ipaddress.ip_network(cidr)

        # Determine prefix length based on the desired number of subnets
        new_prefix_length = network.prefixlen + int(
            math.ceil(math.log(num_networks, 2))
        )

        if new_prefix_length > network.max_prefixlen:
            raise ValueError("Too many subnets for given CIDR block")

        # Calculate subnets and display results
        subnets = list(network.subnets(new_prefix=new_prefix_length))
        display_results(subnets)
        update_status(
            f"Number of Networks: {len(subnets)}"
        )  # Update status bar with subnet count

    except ValueError as e:
        display_error(str(e))


def display_results(subnets):
    for subnet in subnets:
        network_address = f"{subnet.network_address}/{subnet.prefixlen}"
        network_mask = subnet.netmask
        broadcast_address = subnet.broadcast_address
        # NOTE For a /32 subnet it's just a single host.
        if subnet.prefixlen == 32:
            usable_range = f"{network_address}"
        else:
            usable_range = (
                f"{subnet.network_address + 1} - {subnet.broadcast_address - 1}"
            )
        subnet_info = f"Network: {network_address}\nNetmask: {network_mask}\nBroadcast: {broadcast_address}\nUsable Range: {usable_range}"

        subnet_label = tk.Label(
            result_frame,
            text=subnet_info,
            borderwidth=2,
            relief="groove",
            wraplength=300,
        )
        subnet_label.pack(
            pady=3, ipadx=2, ipady=2, fill="both", expand=True, anchor="w"
        )
        # BUG reset scrollable area to top to ensure the frame gets updated correctly.
        canvas.yview_moveto(0)


def main():
    global cidr_entry, networks_entry, result_frame, status_label, canvas
    # main window
    root = tk.Tk()
    root.title("Subnet Planner   -  by: @theros")
    root.geometry("290x400")

    # Top frame
    top_frame = tk.Frame(root)
    top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

    root.grid_columnconfigure(
        0, weight=1
    )  # Make the column containing the frames expandable
    root.grid_rowconfigure(1, weight=1)  # Allow the result area to expand vertically

    # Widgets
    cidr_label = tk.Label(top_frame, text="CIDR Block:", anchor="w")
    cidr_label.grid(row=0, column=0, sticky="w")

    cidr_entry = tk.Entry(top_frame)
    cidr_entry.grid(row=0, column=1, sticky="ew")

    top_frame.grid_columnconfigure(1, weight=1)  # Make the entry field expandable

    networks_label = tk.Label(top_frame, text="Number of Networks:", anchor="w")
    networks_label.grid(row=1, column=0, sticky="w")

    networks_entry = tk.Entry(top_frame)
    networks_entry.grid(row=1, column=1, sticky="ew")

    calculate_button = tk.Button(top_frame, text="Calculate", command=calculate_subnets)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=5)

    # Scrollable result area
    canvas = tk.Canvas(root)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all"),
        ),
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.grid(row=1, column=0, sticky="nsew", padx=5, pady=10)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=1, column=1, sticky="ns")

    # Status bar at the bottom
    status_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor="w")
    status_label.grid(row=2, column=0, sticky="ew", columnspan=2)

    # allow scrolling with mouse wheel
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    result_frame = scrollable_frame

    root.mainloop()


if __name__ == "__main__":
    main()
