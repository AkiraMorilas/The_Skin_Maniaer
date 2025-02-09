
#thanks to AyM2cllE and Ryu Sei from the 10K+ Discord
#because the osumania skinning system is wacky af
#and took me way longer to figure out even with help than open2jam's XML skins that I figured out alone back in the day
#hell I didn't do anything advanced in Soundsphere but I still feel I understand it's skinning more than osu skinning

with open('preset.ini') as f:
    presetfile = list(f)

#remove comments and blank lines
preset = []
for i in presetfile:
    j = i.rstrip()
    if j != '' and j[0] != '#':
        preset.append(j)

#create a list of notes
notes = []
while True:
    name = preset.pop(0)
    if name == '!':
        break
    note = preset.pop(0)
    head = preset.pop(0)
    body = preset.pop(0)
    tail = preset.pop(0)
    keyup = preset.pop(0)
    keydown = preset.pop(0)
    lanecolor = preset.pop(0)
    notes.append([name, note, head, body, tail, keyup, keydown, lanecolor])
#TODO: separate pops are proabably not necessary
#TODO: throw an error if ! is somewhere else than in name
#TODO: and another error if the list ends without it

#get the values that(in most skins anyway, and all of the ones this script supports) don't change with the keycount
skinname = preset.pop(0)
authorname = preset.pop(0)
hitposition = preset.pop(0)
scoreposition = preset.pop(0)
comboposition = preset.pop(0)
width = int(preset.pop(0))
height = int(preset.pop(0))
barline = preset.pop(0)

#create a list of keymodes
keymodes = []
while True:
    lanes = preset.pop(0).split()
    widths = preset.pop(0).split()
    while len(widths) < len(lanes):
        widths.append(widths[0])
    linewidths = preset.pop(0).split()
    while len(linewidths) < len(lanes):
        linewidths.append(linewidths[0])
    lanesplit = preset.pop(0).split()
    keymodes.append([lanes,widths,linewidths,lanesplit])
    if preset == []:
        break
#TODO: this one also assumes no error in the preset file, I should fix that

def list2str(lista):
    r = ''
    for i in lista:
        r += i + ', '
    return r

#generate a ColumnStart: that centers the playfield
def widththings(keymode):
    #the centering formula turns out to be as follows
    #((480 / (screen height / screen width)) / 2) - (sum of all note widths / 2)
    #if I ever support split stages I'd also need to subtract half of the distance between stages from the result
    #went through 4 wrong sources before I found a random screenshot from some chan I don't recognise with this formula
    #and even that didn't mention the split stages thing, I found it out myself while testing
    #because the original skinning tutorial got deleted years ago and "will be replaced" by the skinship(TM) tutorial "soon" lol
    r = ''
    summed = 0
    separator = int(keymode[3][0])
    for i in keymode[1]:
        summed += int(i)
    start = int(((480 / (height / width)) / 2) - (summed / 2))
    if separator > 0:          
        r += "SplitStages: 1\n"
        r += "StageSeparation: " + str(separator) + "\n"
        start = start - int(separator / 2)
    else:
        r += "SplitStages: 0\n"
    r += "ColumnStart: " +  str(start) + "\n"
    return r

def keysearch(key):
    for i in notes:
        if i[0] == key:
            return i

#actually generate the skin
out = "[General]\n"
out += 'Name: ' + skinname + "\n"
out += 'Author: ' + authorname + "\n"
out += "Version: 2.5\n"

for i in keymodes:
    out += "\n[Mania]\nKeys: " + str(len(i[1])) + "\n"
    out += widththings(i)
    out += "ColumnWidth: " + list2str(i[1]) + "\n"
    out += "ColumnLineWidth: " + list2str(i[2]) + "\n"
    out += "HitPosition: " + hitposition + "\n"
    out += "LightPosition: " + hitposition + "\n"
    #counterintuitively, only SOME light effects are tied to HitPosition
    #and of course they happen to be the ones I don't use in my skin
    #so I have to set LightPosition to match HitPositions
    out += "ScorePosition: " + scoreposition + "\n"
    out += "ComboPosition: " + comboposition + "\n"
    out += "BarlineHeight: " + barline + "\n"
    out += "NoteBodyStyle: 0\n\n"
    lanenumber = 0
    for j in i[0]:
        key = keysearch(j)
        out += "NoteImage" + str(lanenumber) + ": " + key[1]  + "\n"
        out += "NoteImage" + str(lanenumber) + "H" + ": " + key[2] + "\n"
        out += "NoteImage" + str(lanenumber) + "L" + ": " + key[3] + "\n"
        out += "NoteImage" + str(lanenumber) + "T" + ": " + key[4] + "\n"
        out += "KeyImage" + str(lanenumber) + ": " + key[5] + "\n"
        out += "KeyImage" + str(lanenumber) + "D" + ": " + key[6] + "\n"
        lanenumber += 1
        #osu skin.ini actually mixes 0-indexed and 1-indexed names for sprites for the same fucking collumn
        #because the original creator of osumania left before finishing the gamemode to create Malody
        #and it was completed by someone else(peppy?)
        #Colour is the only 1-indexed one that I use though
        out += "Colour" + str(lanenumber) + ": " + key[7] + "\n"
        out += "\n"
    
#write the file
f = open("skin.ini", "w")
f.write(out)
f.close()
