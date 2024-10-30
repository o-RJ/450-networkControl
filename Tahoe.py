import pandas as pd
def tahoe(congestion_events):
    events = pd.read_csv('events.csv')
    CWND = 1
    SSTHRESH = 64

    log = []

    for _, event in events.iterrows():
        if event['Event'] == 'Triple Duplicate' or event['Event'] == 'Retransmission':
            SSTHRESH = max(CWND // 2, 1)
            CWND = 1
        elif CWND < SSTHRESH:
            CWND *= 2
        else:
            CWND += 1

        log.append({
            'Timestamp': event['Timestamp'],
            'Event': event['Event'],
            'cwnd': CWND,
            'sshthresh': SSTHRESH
        })

    pd.DataFrame(log).to_csv('tahoe_cwnd.csv', index=False)
    print(f"Tahoe congestion control log saved to tahoe_cwnd.csv")