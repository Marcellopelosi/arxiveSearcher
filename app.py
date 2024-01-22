import pandas as pd
import urllib
import requests
import numpy as np
from itertools import combinations
import streamlit as st

def arxive_searcher(keywords_list):
  """Return a df retrieving results from arxive.org, according to ALL the words in the keywards list. First 20 results"""

  elaborated_keywords = "+AND+".join(["all:"+ k.replace(" ","%20") for k in keywords_list])
  url = "http://export.arxiv.org/api/query?search_query=" + elaborated_keywords + "&max_results=20"
  data = urllib.request.urlopen(url)
  try:
    df = pd.read_xml(data.read().decode('utf-8', "replace"))[["title","summary", "doi", "published"]]
    df = df.dropna(subset = "summary").sort_values(by = "published", ascending = False).reset_index(drop = True)
  except KeyError:
    df = pd.DataFrame(columns = ["title","summary", "doi", "published"] )
  return df

def make_clickable(title):
    return '<a href="https://www.google.it/search?q={}" rel="noopener noreferrer" target="_blank">{}</a>'.format("+".join(title.split()),title)

def enhanced_arxive_searcher(keywords, percentage = 0.7):

  answers = []
  for keywords_subset in combinations(keywords, int(len(keywords)*percentage)):
    answers.append(arxive_searcher(keywords_subset).head(5))

  answer = pd.concat(answers).reset_index(drop = True)
  answer = answer.drop_duplicates()
  answer = answer.sort_values(by = "published", ascending = False).reset_index(drop = True)

  return answer

st.title("Arxive search engine")
st.write("Search engine for Arxiv. Changes results and search order from traditional search. Starting from a list of keywords provided as input. Ideal for searches with a large number of keywords.") 
         
Translated with DeepL.com (free version))
# Create a session state to store the keyword list
if 'keyword_list' not in st.session_state:
    st.session_state.keyword_list = []

new_keyword = st.text_input("Add your keywords (comma separated list):")

if st.button("Add Keywords") and new_keyword:
    st.session_state.keyword_list = [k.strip() for k in new_keyword.split(",")]

if st.button("Delete keywords") and st.session_state.keyword_list:
    st.session_state.keyword_list = []

st.write("Current Keywords:")
for keyword in st.session_state.keyword_list:
    st.write(f"- {keyword}")

if st.button("Search on Arxive") and st.session_state.keyword_list:
  df = enhanced_arxive_searcher(st.session_state.keyword_list)
  st.write(df)
  st.write("How it works: from the set of keywords provided as input, subsets of size 70% of the main set are processed. The results are put together, duplicates are removed, and finally they are sorted starting with the most recent.")
