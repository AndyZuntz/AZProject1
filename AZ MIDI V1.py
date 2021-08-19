# AZ_Midi_Converter
# Takes a midi file as its argument and returns an AZMiniMidi file



def Create_AZ_MIdi_File(Original_Midi_File):
    import mido
    import numpy as np
    # Import a simple MIDI file
    mid = mido.MidiFile(Original_Midi_File)
    print("Midi File loaded")

    # make a slimmed down list with just the basic data i need
    AZminiMidi = []

    # extract the type and duration info
    for AZtrack in (mid.tracks):
        print("TRACK", AZtrack)
        for AZmsg in AZtrack:
            if AZmsg.type == 'note_on' or AZmsg.type == "note_off":
                AZminiMidi.append(AZmsg.type)
                AZminiMidi.append(int(AZmsg.time))

    # check it looks right
    print("AZminiMidi first 12 elements")

    # how long is the piece?
    no_of_notes = int(len(AZminiMidi) / 2)

    # create a numpy array
    AZMM_Array1 = np.array(AZminiMidi)

    # now  create a new one reshaped
    AZMM_Array2 = AZMM_Array1.reshape(no_of_notes, 2)

    # now turn it into an integer array called AZMM_Integer temp filled with 99
    AZMM_Integer = np.full((no_of_notes, 2), 99)
    for i in range(0, no_of_notes-1):

        #  insert the note duration  as an integer

        AZMM_Integer[i, 1] = int(AZMM_Array2[i, 1])

        # convert on and off to 1 and 0

        if AZMM_Array2[i, 0] == 'note_on':
            AZMM_Integer[i, 0] = 1
        elif AZMM_Array2[i, 0] == 'note_off':
            AZMM_Integer[i, 0] = 0
    # need to create some silence at the end of each note.
    #  take it off the 'off' command and add it to the next 'on'
    silence = .1   #out of 1.0
    AZMM_Integer_Detached_Notes = np.full((no_of_notes, 2), 99)
    # Start the first note
    AZMM_Integer_Detached_Notes[0, 0] = AZMM_Integer[0, 0]
    AZMM_Integer_Detached_Notes[0, 1] = AZMM_Integer[0, 1]
    for x in range(1, no_of_notes-1,2):
        AZMM_Integer_Detached_Notes[x, 0] = AZMM_Integer[x, 0]
        AZMM_Integer_Detached_Notes[x,1] = AZMM_Integer[x,1]*(1-silence)

        silent_period = AZMM_Integer[x,1]*silence
        AZMM_Integer_Detached_Notes[x+1,1] = AZMM_Integer[x+1,1] + silent_period
        AZMM_Integer_Detached_Notes[x + 1, 0] = AZMM_Integer[x + 1, 0]

    # Finally, create the cumulative array, where each event is given its absolute time position.
    AZMM_Cumulative__Integer_Detached_Notes = np.full((no_of_notes, 2), 99)
    # Start the first note
    AZMM_Cumulative__Integer_Detached_Notes[0] = AZMM_Integer_Detached_Notes[0]
    for x in range (1,no_of_notes-1):
        AZMM_Cumulative__Integer_Detached_Notes[x,0]=AZMM_Integer_Detached_Notes[x,0]
        AZMM_Cumulative__Integer_Detached_Notes[x, 1] = AZMM_Integer_Detached_Notes[x, 1]+ AZMM_Cumulative__Integer_Detached_Notes[x-1,1]

    for x in range(0, no_of_notes):
        print(AZMM_Cumulative__Integer_Detached_Notes [x])


def main():
    print("This is the main Program")
    
    print("Stage 1, Convert a midi file  ")
    Create_AZ_MIdi_File("entertainer.mid")

if __name__ == "__main__":
    main()