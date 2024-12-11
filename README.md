# DAIRHuM

This is a proof-of-concept system implementation that was used to experimentally study human-AI Alignment in Carnatic music.

The supporting code and documentation are provided in this repository:

1) run_app.py - To recreate the results reported in the submitted manuscript.

2) src/prepare.py - Create and save embeddings from raw audio files using pretrained models (Wavenet)

3) src/create_stats_table.py - Compare embeddings to compute Alignment

## Instructions to run:

Using the following instructions, the project can be run on the terminal: 

>> git clone https://github.com/prashanthtr/DAIRHuM.git
>> uv sync 
>> uv run run_app.py

## Testing alignment for multiple recordings

## Use your own recordings
