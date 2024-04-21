def melodic_evaluation(modes):
    gt_intervals = [
        ['1', '2', 'b3', '4', '5', '6', '7'],
        ['1', 'b2', 'b3', '4', '5', '6', 'b7'],
        ['1', '2', '3', '#4', '#5', '6', '7'],
        ['1', '2', '3', '#4', '5', '6', 'b7'],
        ['1', '2', '3', '4', '5', 'b6', 'b7'],
        ['1', '2', 'b3', '4', 'b5', 'b6', 'b7'],
        ['1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7']
    ]

    print('=== Intervals: ==')

    # Print which values from modes.intervals are different than gt_intervals
    for i in range(7):
        if modes.intervals[i] != gt_intervals[i]:
            print(f"Mode {i+1} is different")
            print(f"Expected: {gt_intervals[i]}")
            print(f"Got:      {modes.intervals[i]}")
            print()
        else:
            print(f"Mode {i+1} is correct")
            print()

    string_chords = """Cm7M	Dm7	Eb7M(#5)	F7	G7	Am7(b5)	Bm7(b5)
    Cm7	Db7M(#5)	Eb7	F7	Gm7(b5)	Am7(b5)	Bbm7M
    C7M(#5)	D7	E7	F#m7(b5)	G#m7(b5)	Am7M	Bm7
    C7	D7	Em7(b5)	F#m7(b5)	Gm7M	Am7	Bb7M(#5)
    C7	Dm7(b5)	Em7(b5)	Fm7M	Gm7	Ab7M(#5)	Bb7
    Cm7(b5)	Dm7(b5)	Ebm7M	Fm7	Gb7M(#5)	Ab7	Bb7
    Cm7(b5)	Dbm7M	Ebm7	Fb7M(#5)	Gb7	Ab7	Bbm7(b5)"""

    # Split string_chords into a list of lists
    gt_chords = [line.split() for line in string_chords.split('\n')]
    gt_chords
    print('\n==== Chords: ====')
    # Print which chords from modes.chords are different than gt_chords
    for i in range(7):
        if modes.chords[i] != gt_chords[i]:
            print(f"Mode {i+1} is different")
            print(f"Expected: {gt_chords[i]}")
            print(f"Got:      {modes.chords[i]}")
            print()
        else:
            print(f"Mode {i+1} is correct")
            print()