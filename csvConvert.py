import pyshark
import pandas as pd

#indicate our pcap file
pcap_in = "placeholder.pcap"
csv_output = "output.csv"

#make our data a list
data = []

#get the pcap file and filter via tcp.
cap = pyshark.FileCapture(pcap_in, display_filter="tcp")

#loop through the data in the pcap, and if it exists, it will be added to our data list
for packet in cap:
    try:
        timestamp = packet.sniff_time
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        src_port = packet.tcp.srcport
        dst_port = packet.tcp.dstport
        seq = packet.tcp.seq
        ack = packet.tcp.ack
        window_size = packet.tcp.window_size_value
        flags = packet.tcp.flags

        data.append([timestamp, src_ip, dst_ip, src_port, dst_port, seq, ack, window_size, flags])

    except AttributeError:
        continue
#we take our data list and convert it to a pandas DataFrame, with correct column names for the data to fit under
df = pd.DataFrame(data, columns=["Timestamp", "Source IP", "Destination IP", "Source Port", "Destination Port",
                                 "Sequence", "Ack Number", "Window", "Flags"])
#we take our dataframe and use the built in to_csv function to save it to a CSV file
df.to_csv(csv_output, index=False)