from pyknon.music import *
from pyknon.genmidi import *
import weather_data

NOTES = {
    "C":0,
    "Csharp":1,
    "Dflat":2,
    "D":2,
    "Dsharp":3,
    "Eflat":3,
    "E":4,
    "F":5,
    "Fsharp":6,
    "Gflat":6,
    "G":7,
    "Gsharp":8,
    "Aflat":8,
    "A":9,
    "Asharp":10,
    "Bflat":10,
    "B":11
}

### musical things
def major_chord(root,octave,duration):
    return [
        Note(root,octave,dur=duration),
        Note(root+4,octave,dur=duration),
        Note(root+7,octave,dur=duration)
    ]

chord = major_chord(1,4,0.25)
chord2 = major_chord(NOTES["Csharp"],5,0.25)

### beat 1
beat1_top = []
for i in range(4):
    beat1_top.append(Note(NOTES["A"],4,0.25, volume=60))
beat1_bottom = [Rest(0.625), Note(NOTES["E"],5,0.125), Rest(0.125), Note(NOTES["E"],5,0.125)]

for i in range(6):
    beat1_top+=beat1_top
    beat1_bottom+=beat1_bottom

b1_seq_top = NoteSeq(beat1_top)
b1_seq_bottom = NoteSeq(beat1_bottom)
'''b1_midi = Midi(number_tracks=3, instrument=[115,115,116], tempo=110)
b1_midi.seq_notes(b1_seq_top,track=0)
b1_midi.seq_notes(b1_seq_bottom,track=1)
b1_midi.seq_notes(b1_seq_top,track=2)'''
#b1_midi.write("music.mid")

### beat 2
beat2_1 = []
for i in range(8):
    beat2_1.append(Note(NOTES["G"],5,0.125,volume=40))
    beat2_1.append(Rest(0.125))

beat2_2 = [
    Note(NOTES["C"],4,0.125),
    Rest(0.0625),
    Note(NOTES["C"],4,0.0625),
    Note(NOTES["C"],4,0.125),
    Rest(0.125),

    Note(NOTES["C"],4,0.0620),
    Note(NOTES["C"],4,0.0630),
    Rest(0.0625),
    Note(NOTES["C"],4,0.0625),
    Note(NOTES["C"],4,0.125),
    Rest(0.125),
]
beat2_2+=beat2_2

beat2_3 = []
for i in range(16):
    beat2_3.append(Note(NOTES["C"],5,0.0625,volume=60))
    beat2_3.append(Rest(0.0625))

for i in range(5):
    beat2_1+=beat2_1
    beat2_2+=beat2_2
    beat2_3+=beat2_3

b2_seq_1 = NoteSeq(beat2_1)
b2_seq_2 = NoteSeq(beat2_2)
b2_seq_3 = NoteSeq(beat2_3)
"""b2_midi = Midi(number_tracks=3, instrument=[113,116,117], tempo = 65)
b2_midi.seq_notes(b2_seq_1,track=0)
b2_midi.seq_notes(b2_seq_2,track=1)
b2_midi.seq_notes(b2_seq_3,track=2)"""
#b2_midi.write("music.mid")

### beat 3
beat3_1 = [
    #Note(NOTES["C"],4,0.5),
    #Note(NOTES["C"],4,0.5)
    Rest(0.75),
    Note(NOTES["C"],3,0.25)
    ]
#for i in range(2):
#    beat3_1.append(Note(NOTES["A"],4,0.5,volume=100))

beat3_2 = []
for i in range(8):
    beat3_2.append(Note(NOTES["C"],7,0.125,volume=30))

beat3_3 = [
    Rest(0.75),
    Note(NOTES["C"],3,0.25)
]

beat3_4 = [
    Note(NOTES["A"],4,0.25),
    Rest(0.25),
    Note(NOTES["A"],4,0.25),
    Rest(0.25)
]

for i in range(6):
    beat3_4+=beat3_4
    beat3_3+=beat3_3
    beat3_2+=beat3_2

#[116,115,115]

b3_seq_1 = NoteSeq(beat3_1)
b3_seq_2 = NoteSeq(beat3_2)
b3_seq_3 = NoteSeq(beat3_3)
b3_seq_4 = NoteSeq(beat3_4)
'''
b3_midi = Midi(number_tracks=13, instrument=[115,115,116], tempo = 120)
#b3_midi.seq_notes(b3_seq_1,track=0)
b3_midi.seq_notes(b3_seq_2,track=0)
b3_midi.seq_notes(b3_seq_3,track=1)
b3_midi.seq_notes(b3_seq_4,track=2)
#b3_midi.write("music.mid")
'''
'''
def play(category):
    if category=="thunderstorm" or category=="clouds":
        b2_midi.write("music.mid")
    elif category=="rain" or category=="drizzle" or category=="snow":
        b3_midi.write("music.mid")
    else:
        b1_midi.write("music.mid")
'''

def play(w):
    data = w.get_weather()
    print(data)
    instrs = [41,40,42,32,46,24,74,73,70,68,60,65,57,56,58,22,0,12,13,89,96,94,101,9]
    #instrument = int(str(data["time"]["percent"]).replace(".",''))%104
    instrument = instrs[data["time"]["hour"]-1]
    tempo = None
    midi = None
    if data["category"]=="Thunderstorm" or data["category"]=="Clouds":
        #b2_midi.write("music.mid")
        tempo = 65
        b2_midi = Midi(number_tracks=4, instrument=[113,116,117,instrument], tempo = 65)
        b2_midi.seq_notes(b2_seq_1,track=0)
        b2_midi.seq_notes(b2_seq_2,track=1)
        b2_midi.seq_notes(b2_seq_3,track=2)
        midi = b2_midi
    elif data["category"]=="Rain" or data["category"]=="Drizzle" or data["category"]=="Snow":
        #b3_midi.write("music.mid")
        tempo = 120
        b3_midi = Midi(number_tracks=4, instrument=[115,115,116,instrument], tempo = 120)
        b3_midi.seq_notes(b3_seq_2,track=0)
        b3_midi.seq_notes(b3_seq_3,track=1)
        b3_midi.seq_notes(b3_seq_4,track=2)
        midi = b3_midi
    else:
        #b1_midi.write("music.mid")
        tempo = 110
        b1_midi = Midi(number_tracks=4, instrument=[115,115,116,instrument], tempo=110)
        b1_midi.seq_notes(b1_seq_top,track=0)
        b1_midi.seq_notes(b1_seq_bottom,track=1)
        b1_midi.seq_notes(b1_seq_top,track=2)
        midi = b1_midi

    #octave = int(data["time"]["percent"]*10)
    octave=5
    #instrument = int(data["time"]["sunrise"]%128)
    rhythm0 = [0.125,0.125,0.25,0.125,0.125,0.25]
    rhythm1 = [0.125,0.25,0.125,0.25,0.25]
    rhythm2 = [0.0625,0.0625,0.0625,0.0625,0.125,0.125,0.25,0.25]
    possible_rhythms = [rhythm0,rhythm1,rhythm2]
    #rhythm = possible_rhythms[data["humidity"]%3]
    rhythm = rhythm0+rhythm0+rhythm2+rhythm1
    pitches = str(data["temp"]).replace('.','')
    notes = []
    for i in range(len(rhythm)):
        notes.append(Note(value=int(pitches[i%len(pitches)]),octave=octave,dur=rhythm[i],volume=60))
    for i in range(4):
        notes+=notes
    seq = NoteSeq(notes)
    midi.seq_notes(seq,track=3)
    midi.write("./building-an-app/music.mid")

test = weather_data.WeatherData("chicago", "city")

play(test)
