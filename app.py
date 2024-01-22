import pandas as pd
import urllib
import requests
import numpy as np
from itertools import combinations
import streamlit as st

def arxive_searcher(keywords_list):
  """Return a df retrieving results from arxive.org, according to ALL the words in the keywards list. First 20 results"""

  elaborated_keywords = "+AND+".join(["all:"+ k for k in keywords_list])
  url = "http://export.arxiv.org/api/query?search_query=" + elaborated_keywords + "&max_results=20"
  data = urllib.request.urlopen(url)
  try:
    df = pd.read_xml(data.read().decode('utf-8', "replace"))[["title","summary", "doi", "published"]]
    df = df.dropna(subset = "summary").sort_values(by = "published", ascending = False).reset_index(drop = True)
  except KeyError:
    df = pd.DataFrame(columns = ["title","summary", "doi", "published"] )
  return df

def enhanced_arxive_searcher(keywords, percentage = 0.7):

  answers = []
  for keywords_subset in combinations(keywords, int(len(keywords)*percentage)):
    answers.append(arxive_searcher(keywords_subset).head(5))

  answer = pd.concat(answers).reset_index(drop = True)
  answer = answer.drop_duplicates()
  answer = answer.sort_values(by = "published", ascending = False).reset_index(drop = True)

  return answer

keywords = []
keywords.append(st.text_input("Add a keyword"))
st.write("Selected Keywords:")
st.write(keywords)

df = enhanced_arxive_searcher(keywords)
st.write(df)



