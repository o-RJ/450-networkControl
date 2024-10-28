import pandas as pd

#load our csv
csv_path = "placeholder.csv"
df = pd.read_csv(csv_path)

#sort by timestamp
df.sort_values(by='timestamp', inplace=True)

#we will store the congestion events in a list
congestion_events = []

#check the rows for congestion
for i in range(2, len(df)):
    #triple dup
    if (
        df.iloc[i]["Ack NUMBER"] == df.iloc[i-1]["Ack NUMBER"] == df.iloc[i-2]["Ack NUMBER"]
        and df.iloc[i]["Sequence"] == df.iloc[i-1]["Sequence"]
    ):
        congestion_events.append({
            'Event': 'Triple Duplicate',
            'Timestamp': df.iloc[i]['timestamp'],
            'Ack Number': df.iloc[i]['Ack Number'],
            'Sequence': df.iloc[i]['Sequence']
        })
    if df.iloc[i]["Sequence"] == df.iloc[i-1]["Sequence"]:
        congestion_events.append({
            'Event': 'Retransmission',
            'Timestamp': df.iloc[i]['timestamp'],
            'Ack Number': df.iloc[i]['Ack Number'],
            'Sequence': df.iloc[i]['Sequence']
        })

congestion_df = pd.DataFrame(congestion_events)

congestion_csv = 'congestion_events.csv'
congestion_df.to_csv(congestion_csv, index=False)

print(f"Congestion events saved to {congestion_csv}")