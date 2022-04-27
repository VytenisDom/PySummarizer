## PySummarizer

A simple way to summarize texts

## How to install
1) Clone or download and extract
2) Install dependencies and Python3 (if not yet installed)
3) Launch from terminal

## How to use
- The program must be run with four parameters - InputMode, OutputMode, Source and N
-   InputMode:
    - [0] - Load text from file
    - [1] - Load text from terminal
-   OutputMode:
    - [0] - Output text to file
    - [1] - Output text to console
-   Source:
    - [./filepath/filename.extension] - Used if InputMode = 0, Input text will be loaded from this file.
    - ["AnyString"] - Used if InputMode = 0, Input text will be loaded from string
-   N:
    - [integer] - Set a number of sentences to be returned.
    - [float < 1] - Set a percentage of text to be returned (calculated as % of total sentences)
