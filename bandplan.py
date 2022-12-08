# bandplan.py

BEACON_BAND_LIST_INDEX = 0
WIDE_BAND_LIST_INDEX = 1
NARROW_BAND_LIST_INDEX = 2
V_NARROW_BAND_LIST_INDEX = 3

BAND_LIST = [
    'Beacon',
    'Wide',
    'Narrow',
    'V.Narrow',
]
BEACON_FREQUENCY_LIST = [
    '10491.50 / --',
]
WIDE_FREQUENCY_LIST = [
    '10493.25 / 03',
    '10494.75 / 09',
    '10496.25 / 15',
]
NARROW_FREQUENCY_LIST = [
    '10492.75 / 01',
    '10493.25 / 03',
    '10493.75 / 05',
    '10494.25 / 07',
    '10494.75 / 09',
    '10495.25 / 11',
    '10495.75 / 13',
    '10496.25 / 15',
    '10496.75 / 17',
    '10497.25 / 19',
    '10497.75 / 21',
    '10498.25 / 23',
    '10498.75 / 25',
    '10499.25 / 27', # _f_index 13
]
V_NARROW_FREQUENCY_LIST = [
    '10492.75 / 01',
    '10493.00 / 02',
    '10493.25 / 03',
    '10493.50 / 04',
    '10493.75 / 05',
    '10494.00 / 06',
    '10494.25 / 07',
    '10494.50 / 08',
    '10494.75 / 09',
    '10495.00 / 10',
    '10495.25 / 11',
    '10495.50 / 12',
    '10495.75 / 13',
    '10496.00 / 14',
    '10496.25 / 15',
    '10496.50 / 16',
    '10496.75 / 17',
    '10497.00 / 18',
    '10497.25 / 19',
    '10497.50 / 20',
    '10497.75 / 21',
    '10498.00 / 22',
    '10498.25 / 23',
    '10498.50 / 24',
    '10498.75 / 25',
    '10499.00 / 26',
    '10499.25 / 27',
]
BEACON_SYMBOL_RATE_LIST = [ 
    '1500',
]
WIDE_SYMBOL_RATE_LIST = [
    'AUTO',
    '500',
    '1000',
    '1500',
]
NARROW_SYMBOL_RATE_LIST = [
    'AUTO',
    '125',
    '250',
    '333',
]
V_NARROW_SYMBOL_RATE_LIST = [
    'AUTO',
    '25',
    '33',
    '66',
]

class BandPlan():
    def __init__(self):
        self._b_index = 0
        self._f_index = 0
        self._s_index = 0
        self._prev_band = 0
        self._prev_wide_f_index = 0
        self._prev_wide_s_index = 0
        self._prev_narrow_f_index = 0
        self._prev_narrow_s_index = 0
        self._prev_v_narrow_f_index = 0
        self._prev_v_narrow_s_index = 0
        self._change_band()
        self._update_variables()

    def _update_variables(self):
        self.band = BAND_LIST[self._b_index]
        self.frequency = self._curr_frequency_list[self._f_index]
        self.symbol_rate = self._curr_symbol_rate_list[self._s_index]
        self.changed = True

    def _change_band(self):
        if self._b_index == BEACON_BAND_LIST_INDEX:
            self._curr_frequency_list = BEACON_FREQUENCY_LIST
            self._f_index = 0
            self._curr_symbol_rate_list = BEACON_SYMBOL_RATE_LIST
            self._s_index = 0
        elif self._b_index == WIDE_BAND_LIST_INDEX:
            self._curr_frequency_list = WIDE_FREQUENCY_LIST
            self._f_index = self._prev_wide_f_index
            self._curr_symbol_rate_list = WIDE_SYMBOL_RATE_LIST
            self._s_index = self._prev_wide_s_index
        elif self._b_index == NARROW_BAND_LIST_INDEX:
            self._curr_frequency_list = NARROW_FREQUENCY_LIST
            self._f_index = self._prev_narrow_f_index
            self._curr_symbol_rate_list = NARROW_SYMBOL_RATE_LIST
            self._s_index = self._prev_narrow_s_index
        elif self._b_index == V_NARROW_BAND_LIST_INDEX:
            self._curr_frequency_list = V_NARROW_FREQUENCY_LIST
            self._f_index = self._prev_v_narrow_f_index
            self._curr_symbol_rate_list = V_NARROW_SYMBOL_RATE_LIST
            self._s_index = self._prev_v_narrow_s_index

    def dec_band(self):
        self._prev_b_index = self._b_index
        if self._b_index > 0:
            self._b_index -= 1
            self._change_band()
            self._update_variables()

    def inc_band(self):
        if self._b_index < len(BAND_LIST) - 1:
            self._b_index += 1
            self._change_band()
            self._update_variables()

    def dec_frequency(self):
        if self._f_index > 0:
            self._f_index -= 1
            self._update_variables()

    def inc_frequency(self):
        if self._f_index < len(self._curr_frequency_list) - 1:
            self._f_index += 1
            self._update_variables()

    def dec_symbol_rate(self):
        if self._s_index > 0:
            self._s_index -= 1
            self._update_variables()

    def inc_symbol_rate(self):
        if self._s_index < len(self._curr_symbol_rate_list) - 1:
            self._s_index += 1
            self._update_variables()

    def fequency_and_rate_list(self):
        if self.symbol_rate == 'AUTO':
            rate_list = self._curr_symbol_rate_list
            rate_list.remove("AUTO")
        else:
            rate_list = [self.symbol_rate]
        return self.frequency[:8], rate_list



band_plan = BandPlan()



######## For TxTouch ###########################################################

TX_FREQUENCY_LIST = [
    '2403.25 / 1',
    '2403.50 / 2',
    '2403.75 / 3',
    '2404.00 / 4',
    '2404.25 / 5',
    '2404.50 / 6',
    '2404.75 / 7',
    '2405.00 / 8',
    '2405.25 / 9',
    '2405.50 / 10',
    '2405.75 / 11',
    '2406.00 / 12',
    '2406.25 / 13',
    '2406.50 / 14',
    '2406.75 / 15',
    '2407.00 / 16',
    '2407.25 / 17',
    '2407.50 / 18',
    '2407.75 / 19',
    '2408.00 / 20',
    '2408.25 / 21',
    '2408.50 / 22',
    '2408.75 / 23',
    '2409.00 / 24',
    '2409.25 / 25',
    '2409.50 / 26',
    '2409.75 / 27',
]
SYMBOL_RATE_LIST = [
    '25',
    '33',
    '66',
    '125',
    '250',
    '333',
    '500',
    '1000',
    '1500',
]
FEC_LIST = [
    '1/2',
    '2/3',
    '3/4',
    '4/5',
    '5/6',
    '6/7',
    '7/8',
    '8/9',
]
MODE_SEL_LIST = {
    'DVB-S',
    'DVB-S2',
}
MODE_LIST = [
    'Initialising',
    'Searching',
    'Found Headers',
    'Locked DVB-S',
    'Locked DVB-S2',
]
CODEC_LIST = [
    'H264 ACC',
    'H265 ACC',
]
CONSTELLATION_LIST = [
    'QPSK',
    '8PSK',
    '16PSK',
    '32PSK',
]
