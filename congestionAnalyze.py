import pandas as pd

def analyze_congestion(csv_path):
    #load our csv
    df = pd.read_csv(csv_path)

    #sort by timestamp
    df = df.sort_values(by='Timestamp')

    #we will store the congestion events in a list
    congestion_events = []

    #last event tag so that we dont have sequential events on accident
    last_event = None
    #these functions both modify the congest events list
    triple_duplicate(df,congestion_events)
    retransmission(df, congestion_events)

    congestion_df = pd.DataFrame(congestion_events)
    congestion_csv = 'congestion_events.csv'
    congestion_df.to_csv(congestion_csv, index=False)
    print(f"Congestion events saved to {congestion_csv}")

def triple_duplicate(df,congestion_events):
    last_ack = None
    duplicate_count = 0

    #iterate over the rows in the dataframe, using an index row pair (no index needed)
    for _, row in df.iterrows():
        current_ack = row['Ack Number']
        #we check to see if the current is the same as the last ack, if yes, we count it as a duplicate
        if current_ack == last_ack:
            duplicate_count += 1
        else:
            #if its different we reset the counter and start again
            duplicate_count = 1
            last_ack = current_ack
        #if it is a triple duplicate, we add it to our congestion events list
        if duplicate_count == 3:
            congestion_events.append({
                'Event': 'Triple Duplicate',
                'Timestamp': row['Timestamp'],
                'Ack Number': row['Ack Number'],
                'Sequence': row.get(('Sequence'))
            })
            duplicate_count = 0

def retransmission(df, congestion_events):
    seen = {} #key value pair dictionary for checking
    #use the index to iterate over the dataframe
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
    dup_tag = set()  # to avoid duplicate tagging
    packets['Congestion Event'] = ''
    # add congestion event to matching packets in wireshark_dataframe.csv
    for _, event in congestion_events.iterrows():
        matching = (packets['Timestamp'] == event['Timestamp']) & \
                   (packets['Ack Number'] == event['Ack Number']) &\
                    (packets['Sequence'] == event['Sequence'])
        matching_events = packets[matching]
        #dont duplicate tagging (will make most events show as retransmission otherwise)
        if not matching_events.empty:
            for idx in matching_events.index:
                keyw = (event['Timestamp'], event['Ack Number'])
                if keyw not in dup_tag:
                    packets.loc[idx, 'Congestion Event'] = event['Event']
                    dup_tag.add(keyw)

    packets.to_csv('congestion_gold.csv', index=False)
    print("Congestion info added to congestion_gold.csv")