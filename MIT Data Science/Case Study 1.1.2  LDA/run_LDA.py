# Script to  actually run the LDA analysis

import LDA as lda
import urllib.request
from bs4 import BeautifulSoup
import os
import re

# Override one prof
prof = 'Elfar Adalsteinsson'

# print(lda.read_abstracts(prof))

lda.save_abstracts()

