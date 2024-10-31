import pandas as pd

def analyze_congestion(csv_path):
    #load our csv
    df = pd.read_csv(csv_path)

    #sort by timestamp
    df.sort_values(by='Timestamp', inplace=True)

    #we will store the congestion events in a list
    congestion_events = []

    last_event = None
    triple_duplicate(df,congestion_events)
    retransmission(df, congestion_events)

    congestion_df = pd.DataFrame(congestion_events)
    congestion_csv = 'congestion_events.csv'
    congestion_df.to_csv(congestion_csv, index=False)
    print(f"Congestion events saved to {congestion_csv}")

def triple_duplicate(df,congestion_events):
    last_ack = None
    duplicate_count = 0

    for _, row in df.iterrows():
        current_ack = row['Ack Number']

        if current_ack == last_ack:
            duplicate_count += 1
        else:
            duplicate_count = 1
            last_ack = current_ack

        if duplicate_count == 3:
            congestion_events.append({
                'Event': 'Triple Duplicate',
                'Timestamp': row['Timestamp'],
                'Ack Number': row['Ack Number'],
                'Sequence': row.get(('Sequence'))
            })
            duplicate_count = 0

def retransmission(df, congestion_events):
    seen = {}

    for idx, row in df.iterrows():
        key = (row['Source IP'], row['Destination IP'], row['Source Port'], row['Destination Port'], row['Sequence'])

        if key in seen:
            congestion_events.append({
                'Event': 'Retransmission',
                'Timestamp': row['Timestamp'],
                'Ack Number': row['Ack Number'],
                'Sequence': row.get(('Sequence'))
            })
        else:
            seen[key] = row['Timestamp']

def add_congestion_info(wireshark_path, congestion_csv):
    packets = pd.read_csv(wireshark_path)
    congestion_events = pd.read_csv(congestion_csv)
    dup_tag = set()
    packets['Congestion Event'] = ''

    for _, event in congestion_events.iterrows():
        matching = (packets['Timestamp'] == event['Timestamp']) & \
                   (packets['Ack Number'] == event['Ack Number']) &\
                    (packets['Sequence'] == event['Sequence'])
        matching_events = packets[matching]

        if not matching_events.empty:
            for idx in matching_events.index:
                keyw = (event['Timestamp'], event['Ack Number'])
                if keyw not in dup_tag:
                    packets.loc[idx, 'Congestion Event'] = event['Event']
                    dup_tag.add(keyw)

    packets.to_csv('congestion_gold.csv', index=False)
    print(f"Congestion info added to congestion_gold.csv")