import pandas as pd
import urllib
import requests
import numpy as np
from itertools import combinations
import streamlit as st

problems = ["Empty dataframe", "Empty dataframe", "Empty dataframe"]
reasons = ["You are using just one keyword", "Non compatible keywords in the same list"]
solutions = ["Enlarge your keywords list!", "Delete unnecessary keywords"]
possible_issues = pd.DataFrame()
possible_issues.index = problems
possible_issues["possible reason"] = reasons
possible_issues["proposed solution"] = solutions

def arxive_searcher(keywords_list):
  """Return a df retrieving results from arxive.org, according to ALL the words in the keywards list. First 20 results"""

  elaborated_keywords = "+AND+".join(["all:"+ str(k).replace(" ","%20") for k in keywords_list])
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

# Set page title and description
st.set_page_config(
    page_title="Arxiv Search Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("Arxiv Search Engine")
st.sidebar.write(
    "Search engine for Arxiv. Changes results and search order from traditional search. "
    "Starting from a list of keywords provided as input. Ideal for searches with a large number of keywords."
)

# Create a session state to store the keyword list
if 'keyword_list' not in st.session_state:
    st.session_state.keyword_list = []

# Input for adding new keywords
new_keyword = st.sidebar.text_input("Add your keywords (comma-separated list):")

# Add Keywords button
if st.sidebar.button("Add Keywords") and new_keyword:
    st.session_state.keyword_list = [k.strip() for k in new_keyword.split(",")]

# Delete Keywords button
if st.sidebar.button("Delete Keywords") and st.session_state.keyword_list:
    st.session_state.keyword_list = []

# Display current keywords in the sidebar
st.sidebar.subheader("Current Keywords:")
for keyword in st.session_state.keyword_list:
    st.sidebar.write(f"- {keyword}")

# Main content area
st.title("Search Results")

# Search on Arxiv button
if st.button("Search on Arxiv") and st.session_state.keyword_list:
    df = enhanced_arxive_searcher(st.session_state.keyword_list)
    st.write("### Results:")
    st.dataframe(df)
    st.write("How it works: from the set of keywords provided as input, subsets of size 70% of the main set are processed. The results are put together, duplicates are removed, and finally they are sorted starting with the most recent.")
    st.subheader("Possible Issues:")
    st.dataframe(possible_issues)
