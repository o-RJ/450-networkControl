from csvConvert import convert
from Tahoe import tahoe
from Renoe import renoe
from congestionAnalyze import analyze_congestion, add_congestion_info

wireshark_path = "./ProjectTrace.pcapng"
convert(wireshark_path)
converted = "wireshark_dataframe.csv"

analyze_congestion(converted)
congestion_csv = "congestion_events.csv"
add_congestion_info(converted, congestion_csv)

congestion_gold = "congestion_gold.csv"

tahoe(congestion_gold)
renoe(congestion_gold)