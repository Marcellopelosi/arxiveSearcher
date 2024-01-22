import pandas as pd
import urllib
import requests
import numpy as np
from itertools import combinations
import streamlit as st

def arxive_searcher(keywords_list):
  """Return a df retrieving results from arxive.org, according to ALL the words in the keywards list. First 20 results"""

  elaborated_keywords = "+AND+".join(["all:"+ k.replace(" ","") for k in keywords_list])
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

# Create a session state to store the keyword list
if 'keyword_list' not in st.session_state:
    st.session_state.keyword_list = []

# Input for adding new keywords
new_keyword = st.text_input("Add a new keyword:")

# Add keyword to the list when the button is clicked
if st.button("Add Keyword") and new_keyword:
    st.session_state.keyword_list.append(new_keyword)

# Delete the last keyword when the button is clicked
if st.button("Delete Last Keyword") and st.session_state.keyword_list:
    deleted_keyword = st.session_state.keyword_list.pop()

# Display the current list of keywords
st.subheader("Current Keywords:")
for keyword in st.session_state.keyword_list:
    st.write(f"- {keyword}")

if st.button("Search on Arxive") and st.session_state.keyword_list:
  df = enhanced_arxive_searcher(st.session_state.keyword_list)
  st.write(df)
