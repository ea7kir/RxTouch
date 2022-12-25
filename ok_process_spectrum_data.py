from dataclasses import dataclass

@dataclass
class SpectrumData:
    beacon_value = 0.0
    spectrum_value = [0] * 918

def process_spectrum_data(recvd_data: bytearray) -> SpectrumData:
    #print(recvd_data)
    spectrum_data = SpectrumData()
    if len(recvd_data) != 1844:
        print('rcvd_data != 1844')
        return spectrum_data
    for i in range(0, 1836, 2):
        uint_16: int = recvd_data[i] + recvd_data[i +1] << 8
        # chop off 1/8 noise
        if uint_16 < 8192: uint_16 = 8192
        spectrum_data.spectrum_value[i // 2] = float(uint_16 - 8192) / 52000.0

    # find the average beacon value where beacon center is 103
    for i in range(73, 133):
        spectrum_data.beacon_value += spectrum_data.spectrum_value[i]
    # invert y axis
    spectrum_data.beacon_value = 1.0 - spectrum_data.beacon_value / 61.0
    #print(spectrum_data.spectrum_value)
    return spectrum_data

#import random
#def test_get_recvd_data():
#    recvd_data = [0] * 1844
#    for i in range(0, 1844):
#        recvd_data[i] = random.randint(100, 6300000)
#    return recvd_data


if __name__ == "__main__":
    import ok_dummy_data
    def get_recvd_data():
        recvd_data = ok_dummy_data.raw_data
        return recvd_data
    #recvd_data = get_recvd_data()
    from ok_net_utils import get_stream_msg
    recvd_data= get_stream_msg()
    spectrum_data = process_spectrum_data(recvd_data)
    print('spectrum_values: ', spectrum_data.spectrum_value)
    print('beacon_value: ', spectrum_data.beacon_value)
    print(len(spectrum_data.spectrum_value))
