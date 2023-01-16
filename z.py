video = {
    #None: '-',
    '2': 'MPEG-2',
    '16': 'H.263',
    '27': 'H.264',
    '36': 'H.265',
}

audio = {
    #None: '-',
    '3': 'MP3',
    '4': 'MP3',
    '15': 'ACC',
    '32': 'MPA',
    '129': 'AC3',
}


print(video.keys())
print(audio.keys())

key = '36'
v = video.get(key)
if v is None:
    v = '?'
print(v)

