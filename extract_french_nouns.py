#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import math
import os
from collections import OrderedDict

# Basic filtering of the entries
MIN_YEAR = 1980 # Ignore all older occurrences
COUNT_THRESHOLD = 500 # Ignore all lesser occurrences

# Template of the regular expression specifying which entries to keep
KEEP_TEMPLATE = ur"^%s_DET [a-záàâäãåçéèêëíìîïñóòôöõúùûüýÿæœ]*?_NOUN$"

# Where and under which names the required Google Ngrams datasets can be found
DIRECTORY = os.path.expanduser("~/Downloads")
NAME_TEMPLATE = "googlebooks-fre-all-2gram-20120701-%s.gz"

# The  CSV files are read by chunks of rows
# WARNING: changing this value may raise an error
# (Pandas issue: https://github.com/pydata/pandas/issues/5291)
CHUNK_SIZE = 99999


def log_progress(sequence, every=None, size=None):
    """Widget based progress bar for Jupyter (IPython Notebook)
    
    Author: Kukushkin Alexander
    Source: https://github.com/alexanderkuk/log-progress
    """

    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = size / 200     # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    label.value = '{index} / ?'.format(index=index)
                else:
                    progress.value = index
                    label.value = u'{index} / {size}'.format(
                        index=index,
                        size=size
                    )
            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = str(index or '?')


# If no HTML logger is available, uncomment the following lines

# def log_progress(sequence, every, size):
#     """Fallback in case the program is run outside Jupyter Notebook."""
#     for (i, element) in enumerate(sequence, 1):
#         if i % every == 0:
#             print "%s/%s" % (i, size)
#         yield element


# Description of the Google Ngrams datasets

sources = [
    {
        "name": "le", # the discriminant part of the filename
        "keep": "[Ll]e", # sub-regexp for the lines to keep
        "discriminant": 1, # position of a character marking the gender
        "masc": "e", # value of this character for the masculine gender
        "masc_start": 7, # first position of a masculine noun
        "row_count": 249600630
    },
    {
        "name": "la",
        "keep": "[Ll]a",
        "discriminant": 1,
        "masc": "e", # no occurrence
        "fem_start": 7, # first position of a feminine noun
        "row_count": 156511945
    },
    {
        "name": "du",
        "keep": "[Dd]u",
        "discriminant": 1,
        "masc": "u", # any occurrence
        "masc_start": 7,
        "row_count":  67674376
    },
    {
        "name": "un",
        "keep": "[Uu]ne?",
        "discriminant": 2,
        "masc": "_", # discriminate "un_" against "une_"
        "masc_start": 7,
        "fem_start": 8,
        "row_count":  89455794
    },
]
dtype = OrderedDict([
    ("digram", unicode),
    ("year", np.int16),
    ("match_count", np.int32),
    ("volume_count", np.int32),
])


# Main program

result = pd.DataFrame()

for source in sources:
    
    # Define an iterator on the current CSV file by chunks of CHUNK_SIZE
    filename = NAME_TEMPLATE % source["name"]
    print filename
    iter_csv = pd.read_csv(
        os.path.join(DIRECTORY, filename),
        encoding="utf8",
        sep="\t",
        iterator=True,
        chunksize=CHUNK_SIZE,
        header=None,
        names=dtype.keys(),
        dtype=dtype
    )
    
    # Construct chunk by chunk  the part corresponding to the current file
    part = pd.DataFrame()
    size = int(math.ceil(source["row_count"] / CHUNK_SIZE))
    for chunk in log_progress(iter_csv, every=1, size=size):
        # Filter the digrams
        part = part.append(chunk[
                  (chunk["year"] >= MIN_YEAR)
                & chunk["digram"].str.match(KEEP_TEMPLATE % source["keep"])
            ])
        
    # Aggregate the occurrence counts by digram
    part = part.groupby("digram").agg({"match_count": "sum"})
    part.reset_index(inplace=True)
    
    # Break down the digrams into the corresponding gender and noun
    part["gender"] = np.where(part["digram"].str.get(source["discriminant"]) == source["masc"], "m", "f")
    part["noun"] = np.where(
        part["gender"] == "m",
        part["digram"].str.slice(source.get("masc_start"), -len("_NOUN")),
        part["digram"].str.slice(source.get("fem_start"), -len("_NOUN"))
    )
    part.drop("digram", axis=1, inplace=True)
    
    # Accumulate the current part
    result = result.append(part)

# Aggregate the occurrence counts by noun and gender
result = result.groupby(["noun", "gender"]).agg({"match_count": "sum"})
result.reset_index(inplace=True)
result.rename(columns={"match_count": "count"}, inplace=True)

# Suppress the nouns having less than COUNT_THRESHOLD occurrences
result = result[result["count"] >= COUNT_THRESHOLD]

# Reorder the columns
result = result[["noun", "gender", "count"]]

# Sort the resulting table by decreasing number of occurrences
result.sort("noun", inplace=True)

# Write the result
result.to_csv("french_nouns.tsv", sep='\t', encoding='utf-8', index=False)
print "Done."

