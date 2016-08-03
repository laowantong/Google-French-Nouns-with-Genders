# A list of french nouns constructed from Google N-Grams

In 2012, Google has published the 2nd version of [a gigantic dataset](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html) of 1-grams, 2-grams, 3-grams, 4-grams, and 5-grams files for several languages, including French.

We can use it to extract a [list of French nouns, along with their gender and frequency](french_nouns.tsv). In a French sentence, when a noun follows “un“, “le“, and “du“ (respectively, “une“ and “la“), it is _generally_ a **masculine** (respectively, **feminine**) noun in the singular form.

To reproduce or modify the generation of this list:

1. Download these four 2-grams archives:
  - http://storage.googleapis.com/books/ngrams/books/googlebooks-fre-all-2gram-20120701-du.gz
  - http://storage.googleapis.com/books/ngrams/books/googlebooks-fre-all-2gram-20120701-le.gz
  - http://storage.googleapis.com/books/ngrams/books/googlebooks-fre-all-2gram-20120701-la.gz
  - http://storage.googleapis.com/books/ngrams/books/googlebooks-fre-all-2gram-20120701-un.gz
  
  Keep them compressed.
1. In the meantime, open `extract_french_nouns.ipynb` (with Jupyter Notebook) or `extract_french_nouns.py` (with any text editor) and edit it to meet your specific needs. For instance, modify the starting year `MIN_YEAR`, the minimal threshold `COUNT_THRESHOLD`, or the path to the `DIRECTORY` where the dataset is downloaded.
1. Launch the program and wait.

## Requirements

You may install [Anaconda](https://www.continuum.io/downloads) which includes all the necessary stuff. Otherwise, install:

- [Python 2.7](https://www.python.org/downloads/).
- [Pandas](http://pandas.pydata.org/pandas-docs/stable/install.html).
- [Numpy](http://www.scipy.org/scipylib/download.html).

## Disclaimers

- Linguists hate me: this 1 old weird trick is unlikely to be met with their approbation and support.
- The Google N-grams dataset is ridden with its own [problems](https://en.wikipedia.org/wiki/Google_Ngram_Viewer#Criticism).
- Don't use this list if you are not a native French speaker. There are just too much errors.
- Don't use this list for any scientific work.
