from pyknon.music import *
from pyknon.genmidi import *

#C_note = Note(0, 5, dur=0.25)
#quarter_rest = Rest(0.25)
#A_note = Note(9, 5, 0.25)
#seq = NoteSeq([C_note, A_note, quarter_rest, C_note])
#
#midi = Midi(1, tempo=120)
#midi.seq_notes(seq, track=0)
#midi.write("simple_noteseq.mid")

OCTAVES = [2,3,4,5,6,7,8]
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
### NOTE: working on changing this one
beat1_top = []
for i in range(4):
    beat1_top.append(Note(NOTES["C"],4,0.25))
beat1_bottom = [Rest(0.875), Note(NOTES["G"],4,0.125)]

for i in range(4):
    beat1_top = beat1_top+beat1_top
    beat1_bottom = beat1_bottom+beat1_bottom

b1_seq_top = NoteSeq(beat1_top)
b1_seq_bottom = NoteSeq(beat1_bottom)
b1_midi = Midi(number_tracks=2, instrument=[118,118], tempo=100)
b1_midi.seq_notes(b1_seq_top,track=0)
b1_midi.seq_notes(b1_seq_bottom,track=1)
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

beat2_3 = []
for i in range(16):
    beat2_3.append(Note(NOTES["C"],5,0.0625,volume=60))
    beat2_3.append(Rest(0.0625))

for i in range(4):
    beat2_1+=beat2_1
    beat2_2+=beat2_2
    beat2_3+=beat2_3

b2_seq_1 = NoteSeq(beat2_1)
b2_seq_2 = NoteSeq(beat2_2)
b2_seq_3 = NoteSeq(beat2_3)
b2_midi = Midi(number_tracks=3, instrument=[113,116,117], tempo = 65)
b2_midi.seq_notes(b2_seq_1,track=0)
b2_midi.seq_notes(b2_seq_2,track=1)
b2_midi.seq_notes(b2_seq_3,track=2)
b2_midi.write("music.mid")
