import pandas as pd
def renoe(congestion_events):
    events = pd.read_csv(congestion_events)

    log = []

    CWD = 1
    SSTHRESH = 64

    for _, event in events.iterrows():
        if event['Event'] == 'Triple Duplicate':
            SSTHRESH = max(CWD // 2, 1)
            CWD = SSTHRESH + 3
        elif event['Event'] == 'Retransmission':
            SSTHRESH = max(CWD // 2, 1)
            CWD = 1
        elif CWD < SSTHRESH:
            CWD *= 2
        else:
            CWD += 1

        log.append({
            'Timestamp': event['Timestamp'],
            'Event': event['Event'],
            'cwnd': CWD,
            'sstresh': SSTHRESH
        })

    pd.DataFrame(log).to_csv('reno.csv', index=False)
    print(f"Reno congestion control log saved to reno.csv")