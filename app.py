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

def add_keyword(value):
  if value:
    st.session_state.keyword_list.append(value)
    st.success(f"Keyword '{value}' added!")

# Create a session state to store the keyword list
if 'keyword_list' not in st.session_state:
    st.session_state.keyword_list = []

# Input for adding new keywords with on_change callback
new_keyword = st.text_input("Add a new keyword:", on_change=add_keyword)

st.subheader("Current Keywords:")
for keyword in st.session_state.keyword_list:
    st.write(f"- {keyword}")

# Delete the last keyword when the button is clicked
if st.button("Delete Last Keyword") and st.session_state.keyword_list:
    deleted_keyword = st.session_state.keyword_list.pop()

# df = enhanced_arxive_searcher(keywords)
# st.write(df)



