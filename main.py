from csvConvert import convert
from Tahoe import tahoe
from Renoe import renoe
from congestionAnalyze import analyze_congestion, add_congestion_info

wireshark_path = "./wireshark_802_11.pcap"
convert(wireshark_path)
converted = "wireshark_dataframe.csv"

analyze_congestion(converted)
congestion_csv = "congestion_events.csv"
add_congestion_info(converted, congestion_csv)
