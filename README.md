# chords
Compile chords, measures, song sections, and entire chord charts into JSON

Uses what is hopefully an intuitive input language, see blues.txt and greendolphin.txt for examples.
Write your chart and save as a text file, and compile it to JSON like this:

    import chords
    with open('sourcetext.txt') as f:
      text = f.read()
    
    chart = ChordChart(text)
    chart.get_json()

To get it with indentation for pretty printing, use:
`chart.get_json(pretty=True)`

You can also get JSON for individual chords or measures by using the Chord or Measure class:
`chords.Chord('Cmaj7/E').get_json()`
