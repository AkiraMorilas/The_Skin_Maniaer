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
    notes.append([name, note, head, body, tail, keyup, keydown])
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
    keymodes.append([lanes,widths])
    if preset == []:
        break
#TODO: this one also assumes no error in the preset file, I should fix that

#generate a ColumnStart: that centers the playfield
def widththings(lanewidths):
    r ="\n[Mania]\nKeys: " + str(len(lanewidths)) + "\n"
    #the centering formula turns out to be as follows
    #((480 / (screen height / screen width)) / 2) - (sum of all note widths / 2)
    #if I ever support split stages I'd also need to subtract half of the distance between stages from the result
    #went through 5 wrong sources before I found a random screenshot from some chan I don't recognise with this formula
    #and even that didn't mention the split stages thing, I found it out myself while testing
    #because the original skinning tutorial got deleted years ago and will be replaced by the skinship(TM) tutorial "soon" lol
    summed = 0
    for i in lanewidths:
        summed += int(i)
    r += "ColumnStart: " +  str(int(((480 / (height / width)) / 2) - (summed / 2))) + "\n"
    r += "ColumnWidth: "
    for i in lanewidths:
        r += i + ", "
    r+= "\n"
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
    out += widththings(i[1])
    out += "SplitStages: 0\n"
    out += "HitPosition: " + hitposition + "\n"
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
        out += "\n"
    
#write the file
f = open("skin.ini", "w")
f.write(out)
f.close()
