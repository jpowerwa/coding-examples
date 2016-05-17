# Coding Examples

Welcome to my repository of coding examples. Currently everything is in python, because that the language I have been using for the past eight years or so.


## Timeline

This program solves the problem of generating one or more timelines consisting of ordered events based on multiple partial timelines submitted by reliable witnesses. The goal is to merge the partial timelines to produce the longest possible timelines consisting of strictly-ordered events. If two witnesses observed different events between two known events, those intervening events cannot be strictly ordered, and two merged timelines will be generated.


### Requirements
 
* If the all witnesses remember events in a fully consistent manner, then present a single merged timeline.
* If some of the events can be strictly ordered across partial timelines, then present multiple timelines with events merged to the degree possible.
* If none of the events in the partial timelines events can be merged, then present the original unmodified timelines.


### Files

The solution consists of the following files:

* timeline.py
* logging_for_recursion.py
* test_timeline.py
* data/testcase_\*.json


### Running the tests

1. If your python version is less than 3, `pip install mock`.
2. `python test_timeline.py [-v]`


### Running the script

```
usage: timeline.py [-h] [-v | -V] infile

Combine partial timelines into longest possible sequences of events

positional arguments:
  infile              input filename containing JSON list of ordered event
                      sequences

optional arguments:
  -h, --help          show this help message and exit
  -v, --verbose       info-level output (default: False)
  -V, --very-verbose  debug-level output (default: False)

```

The input file contains the partial timelines in JSON:

```
  [
    ["fight", "gunshot", "fleeing"],
    ["gunshot", "falling", "fleeing"]
  ]
```

Test scenarios are provided in the data directory:

```
python timeline.py data/testcase_shooting.json -v
```

### Implementation issues

There is one known issue with the implementation. If the partial timelines diverge in multiple places, the merged timelines do not preserve the correspondence of divergent sections. That is, the some of the merged timelines will contain divergent sections from multiple partial timelines.

For example, consider the input timelines

```
  ["a", "b", "c.1", "d.1", "e", "f", "g.1", "h.1", "i"]
  ["b", "c.2", "d.2", "e", "f", "g.2", "h.2", "i", "j"]
```

The desired output is two merged timelines with merged fronts, middles and ends; one merged timeline should contain the \*.1 events, and the other should contain the \*.2 events:

```
  ["a", "b", "c.1", "d.1", "e", "f", "g.1", "h.1", "i", "j"]
  ["a", "b", "c.2", "d.2", "e", "f", "g.2", "h.2", "i", "j"]
```

Instead, this implementation will generate four merged timelines:

```
  ["a", "b", "c.1", "d.1", "e", "f", "g.1", "h.1", "i", "j"]
  ["a", "b", "c.1", "d.1", "e", "f", "g.2", "h.2", "i", "j"]
  ["a", "b", "c.2", "d.2", "e", "f", "g.1", "h.1", "i", "j"]
  ["a", "b", "c.2", "d.2", "e", "f", "g.2", "h.2", "i", "j"]
```

To maintain the correspondence between sections of the original partial timelines would require an entirely different approach, therefore I am not taking it on at this time.


