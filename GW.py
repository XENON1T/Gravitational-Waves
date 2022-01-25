import numpy as np
import pandas as pd

from tqdm import tqdm

import LowER

class dataset_info:

    def __init__(self, runlist):
        """Takes a runlist and generates datasets it in chronological order"""

        coll = LowER.utils.runDB.get_collection()
        query = {'number': {'$in': runlist}}
        cursor = list(coll.find(query, {'start': 1, 'end': 1, 'number': 1, '_id': 0}))
        dsets = pd.DataFrame(cursor)
        self.dsets = dsets.sort_values(by='start', ascending=False)

    def calc_livetimes(self, runlist):
        livetimes = []
        for i in tqdm(range(0, np.shape(runlist)[0])):
            livetimes.append(LowER.utils.runDB.get_livetime_days([int(self.dsets.number[i]), ], update=True))
    
        self.dsets['livetime'] = livetimes #livetime is in days

    def n_Events(self, df_ER_a, df_ER_b):
        """finding number of events for each run"""

        events = []
        for i in tqdm(range(0, np.shape(self.dsets)[0])):
            events.append(np.shape(df_ER_a[df_ER_a['run_number'] == self.dsets.number[i]])[0] + np.shape(df_ER_b[df_ER_b['run_number'] == self.dsets.number[i]])[0])
    
        self.dsets['n_events'] = events

    def n_Events_low(self, df_ER_a, df_ER_b, limit_l, limit_u):
        """finding number of events in low energy bin for each run"""

        ER_a_events_l = df_ER_a[(df_ER_a['energy']>limit_l) & (df_ER_a['energy']<=limit_u)]
        ER_b_events_l = df_ER_b[(df_ER_b['energy']>limit_l) & (df_ER_b['energy']<=limit_u)]
        events_l = []
        for i in tqdm(range(0, np.shape(self.dsets)[0])):
            events_l.append(np.shape(ER_a_events_l[ER_a_events_l['run_number'] == self.dsets.number[i]])[0] + np.shape(ER_b_events_l[ER_b_events_l['run_number'] == self.dsets.number[i]])[0])
    
        self.dsets['n_events_l'] = events_l

    def n_Events_peak1(self, df_ER_a, df_ER_b, limit_l, limit_u):
        """finding number of events in peak 1 energy bin for each run""" 

        ER_a_events_peak1 = df_ER_a[(df_ER_a['energy']>limit_l) & (df_ER_a['energy']<=limit_u)]
        ER_b_events_peak1 = df_ER_b[(df_ER_b['energy']>limit_l) & (df_ER_b['energy']<=limit_u)]
        events_peak1 = []
        for i in tqdm(range(0, np.shape(self.dsets)[0])):
            events_peak1.append(np.shape(ER_a_events_peak1[ER_a_events_peak1['run_number'] == self.dsets.number[i]])[0] + np.shape(ER_b_events_peak1[ER_b_events_peak1['run_number'] == self.dsets.number[i]])[0])
    
        self.dsets['n_events_peak1'] = events_peak1

    def n_Events_medium(self, df_ER_a, df_ER_b, limit_l, limit_u):
        """finding number of events in medium energy bin for each run""" 

        ER_a_events_m = df_ER_a[(df_ER_a['energy']>limit_l) & (df_ER_a['energy']<=limit_u)]
        ER_b_events_m = df_ER_b[(df_ER_b['energy']>limit_l) & (df_ER_b['energy']<=limit_u)]
        events_m = []
        for i in tqdm(range(0, np.shape(self.dsets)[0])):
            events_m.append(np.shape(ER_a_events_m[ER_a_events_m['run_number'] == self.dsets.number[i]])[0] + np.shape(ER_b_events_m[ER_b_events_m['run_number'] == self.dsets.number[i]])[0])
    
        self.dsets['n_events_m'] = events_m

    def n_Events_peak2(self, df_ER_a, df_ER_b, limit_l, limit_u):
        """finding number of events in peak 2 energy bin for each run""" 

        ER_a_events_peak2 = df_ER_a[(df_ER_a['energy']>limit_l) & (df_ER_a['energy']<=limit_u)]
        ER_b_events_peak2 = df_ER_b[(df_ER_b['energy']>limit_l) & (df_ER_b['energy']<=limit_u)]
        events_peak2 = []
        for i in tqdm(range(0, np.shape(self.dsets)[0])):
            events_peak2.append(np.shape(ER_a_events_peak2[ER_a_events_peak2['run_number'] == self.dsets.number[i]])[0] + np.shape(ER_b_events_peak2[ER_b_events_peak2['run_number'] == self.dsets.number[i]])[0])

        self.dsets['n_events_peak2'] = events_peak2

    def n_Events_high(self, df_ER_a, df_ER_b, limit_l, limit_u):
        """finding number of events in high energy bin for each run""" 

        ER_a_events_u = df_ER_a[(df_ER_a['energy']>limit_l) & (df_ER_a['energy']<=limit_u)]
        ER_b_events_u = df_ER_b[(df_ER_b['energy']>limit_l) & (df_ER_b['energy']<=limit_u)]
        events_u = []
        for i in tqdm(range(0, np.shape(self.dsets)[0])):
            events_u.append(np.shape(ER_a_events_u[ER_a_events_u['run_number'] == self.dsets.number[i]])[0] + np.shape(ER_b_events_u[ER_b_events_u['run_number'] == self.dsets.number[i]])[0])
        
        self.dsets['n_events_u'] = events_u

    def calc_event_rate(self, date_breaks, runlist):
        self.rate_event = []
        self.rate_event_l = []
        self.rate_event_m = []
        self.rate_event_u = []
        self.rate_event_peak1 = []
        self.rate_event_peak2 = []

        for i in tqdm(range(0, np.shape(date_breaks)[0])):
            livetime = 0
            n_event = 0
            n_event_l = 0
            n_event_m = 0
            n_event_u = 0
            n_event_peak1 = 0
            n_event_peak2 = 0

            for j in (range(0, np.shape(runlist)[0])):
                if (self.dsets.start[j].timestamp() - date_breaks[i]) <= (24*3600) and (self.dsets.start[j].timestamp() - date_breaks[i]) >= 0:
                    livetime = livetime + self.dsets.livetime[j]    
                    n_event = n_event + self.dsets.n_events[j]
                    n_event_l = n_event_l + self.dsets.n_events_l[j]
                    n_event_m = n_event_m + self.dsets.n_events_m[j]
                    n_event_u = n_event_u + self.dsets.n_events_u[j]
                    n_event_peak1 = n_event_peak1 + self.dsets.n_events_peak1[j]
                    n_event_peak2 = n_event_peak2 + self.dsets.n_events_peak2[j]

            if livetime == 0:
                self.rate_event.append(0)
                self.rate_event_l.append(0)
                self.rate_event_m.append(0)
                self.rate_event_u.append(0)
                self.rate_event_peak1.append(0)
                self.rate_event_peak2.append(0)
            else:
                #event-rate in events/(year*ton) #1.042 is fiducial volume from lowER paper
                self.rate_event.append(n_event/livetime*365/1.042) 
                self.rate_event_l.append(n_event_l/livetime*365/1.042)
                self.rate_event_m.append(n_event_m/livetime*365/1.042)
                self.rate_event_u.append(n_event_u/livetime*365/1.042)
                self.rate_event_peak1.append(n_event_peak1/livetime*365/1.042)
                self.rate_event_peak2.append(n_event_peak2/livetime*365/1.042)                
    
