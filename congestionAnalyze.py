import pandas as pd

def analyze_congestion(csv_path):
    #load our csv
    df = pd.read_csv(csv_path)

    #sort by timestamp
    df.sort_values(by='Timestamp', inplace=True)

    #we will store the congestion events in a list
    congestion_events = []

    #check the rows for congestion
    for i in range(2, len(df)):
        #triple dup
        if (
            df.iloc[i]["Ack Number"] == df.iloc[i-1]["Ack Number"] == df.iloc[i-2]["Ack Number"]
            and df.iloc[i]["Sequence"] == df.iloc[i-1]["Sequence"]
        ):
            congestion_events.append({
                'Event': 'Triple Duplicate',
                'Timestamp': df.iloc[i]['Timestamp'],
                'Ack Number': df.iloc[i]['Ack Number'],
                'Sequence': df.iloc[i]['Sequence']
            })
        if df.iloc[i]["Sequence"] == df.iloc[i-1]["Sequence"]:
            congestion_events.append({
                'Event': 'Retransmission',
                'Timestamp': df.iloc[i]['Timestamp'],
                'Ack Number': df.iloc[i]['Ack Number'],
                'Sequence': df.iloc[i]['Sequence']
            })
    congestion_df = pd.DataFrame(congestion_events)

    congestion_csv = 'congestion_events.csv'
    congestion_df.to_csv(congestion_csv, index=False)
    print(f"Congestion events saved to {congestion_csv}")

def add_congestion_info(wireshark_path, congestion_csv):
    packets = pd.read_csv(wireshark_path)
    congestion_events = pd.read_csv(congestion_csv)

    packets['Congestion Event'] = ''

    for _, event in congestion_events.iterrows():
        matching = packets[(packets['Timestamp'] == event['Timestamp']) & ((packets['Ack Number'] == event['Ack Number'])) | (packets['Sequence'] == event.get(('Sequence'),None))]
        if not matching.empty:
            packets.loc[matching.index, 'Congestion Event'] = event['Event']

    packets.to_csv('congestion_gold.csv', index=False)
    print(f"Congestion info added to congestion_gold.csv")