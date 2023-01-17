
ES_TYPE = {
    '2': 'MPEG-2', # TODO: too wide for display column
    '3': 'MP3',
    '4': 'MP3',
    '15': 'ACC',
    '16': 'H.263',
    '27': 'H.264',
    '32': 'MPA',
    '36': 'H.265',
    '129': 'AC3',
}
def codec_type_name(type_str):
    match type_str:
        case '2': return 'MPEG-2' # TODO: too wide for display column
        case '3': return 'MP3'
        case '4': return 'MP3'
        case '15': return 'ACC'
        case '16': return 'H.263'
        case '27': return 'H.264'
        case '32': return 'MPA'
        case '36': return 'H.265'
        case '129': return 'AC3'
    return '-'

# ES starting pair
class EsPair:
    one = [False, None]
    two = [False, None]

es_pair = EsPair()

def test(s, rawval):
    match s:
        ###################################################################
        case 16: # The PID numbers themselves are fairly arbitrary, will vary based on the transmitted signal and don't really mean anything in a single program multiplex.
            # In the status stream 16 and 17 always come in pairs, 16 is the PID and 17 is the type for that PID, e.g.
            # This means that PID 257 is of type 27 which you look up in the table to be H.264 and PID 258 is type 3 which the table says is MP3.
            # $16,257 == PID 257 is of type 27 which you look up in the table to be H.264
            # $17,27  meaning H.264
            # $16,258 == PID 258 is type 3 which the table says is MP3
            # $17,3   maeaning MP3
            # The PID numbers themselves are fairly arbitrary, will vary based on the transmitted signal and don't really mean anything in a single program multiplex.
            if not es_pair.one[0]:
               es_pair.one[0] = True
            elif not es_pair.two[0]:
                es_pair.two[0] = True
            #print(16, es_pair.one, es_pair.two)
        case 17: # ES TYPE - Elementary Stream Type (repeated as pair with 16 for each ES)
            if es_pair.one[0] and not es_pair.two[0]:
                es_pair.one[0] = True
                es_pair.one[1] = rawval
            elif es_pair.two[0]:
                es_pair.two[0] = True
                es_pair.two[1] = rawval
            #print(17, es_pair.one, es_pair.two)
            if es_pair.one[0] and es_pair.two[0]:
                codecs = f'{codec_type_name(es_pair.one[1])} {codec_type_name(es_pair.two[1])}'
                print(es_pair.one[1], es_pair.two[1], " -> ", codecs)
                es_pair.one = [False, None]
                es_pair.two = [False, None]
        ###################################################################

test(16,'257')
test(17,'27')
test(16,'258')
test(17,'3')

#print(ES_TYPE.get('27'))