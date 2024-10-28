
def tahoe(congestion_events):
    CWND = 1
    SSHTHRESH = 64

    log = []

    for event in congestion_events:
        if event['Event'] == 'Triple Duplicate' or event['Event'] == 'Retransmission':
            sshthresh = max(CWND // 2, 1)
            CWND = 1
        else:
            if CWND < SSHTHRESH:
                CWND *= 2
            else:
                CWND += 1


        log.append({
            'Timestamp': event['Timestamp'],
            'Event': event['Event Type'],
            'cwnd': CWND,
            'sshtresh': SSHTHRESH
        })