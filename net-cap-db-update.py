import subprocess
import time
import re
import csv
import ipaddress
import sqlite3

# Define the tshark command
tshark_command = [
    "tshark",
    "-i",
    "eth0",
    "-T",
    "fields",
    "-e",
    "ip.src",
    "-e",
    "_ws.col.Info",
    "-c",
    "10",
]


def insert_data(info, ipaddress, status):
    data = [(info, ipaddress, status)]
    conn = sqlite3.connect('net_querie_iot.db')
    c = conn.cursor()
    try:
        c.executemany("INSERT INTO net_queries (info, ipaddress, status) VALUES (?, ?, ?)", data)
        conn.commit()
        print(f"Domain '{info}' with IP addresses {ipaddress} added to the database.")
    except sqlite3.IntegrityError:
        print("data not added to database.")
    finally:
        conn.close()


def run_tshark():
    try:
        output = subprocess.check_output(tshark_command, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    # Split the output by lines
    lines = output.splitlines()

    # Process and print the results
    for line in lines:
        if "Capturing on" not in line and "File:" not in line and not line.strip().startswith("**"):
            # Check if the line contains two tab-separated values
            if line.count('\t') == 1:
                src_ip, info = line.split('\t', 1)  # Split the line by tab to get the two fields
                print(f"IP Address: {src_ip}, Info: {info}")
                insert_data(info, src_ip, status=0)
                print("Data ADDED")
            else:
                print(f"Unexpected format: {line}")

if __name__ == "__main__":
    while True:
        run_tshark()
        # Sleep for 5 minutes (300 seconds) before running tshark again
        time.sleep(60)
