# chords
Compile chords, measures, song sections, and entire chord charts into JSON

### Use
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

### Example Input
Here's part of a sample chart, illustrating the syntax of the input language:
```
Title: Fall Departs

(A)
|C-7        |F7         |Bbmaj7     |Ebmaj7     |
|A-7b5      |D7b9       |G-7        |.          |
```
Names of song sections are in parentheses.  Currently there is no support for repeats, multiple endings, or time signatures, but that will change very soon.  Slash chords are supported.  Put a '.' in a measure if it repeats the chord from the previous measure, otherwise it will just be overlooked by the program.
