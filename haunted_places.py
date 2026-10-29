# =============================================================
# Haunted Places in the USA - Data Analysis Project
# Dataset: TidyTuesday (October 10, 2023)
# Goal: find haunted "hotspots" on a map and analyze
#       the text descriptions to find common ghost keywords
# =============================================================

# %% [1] Load the data
import re                           # regular expressions for text processing
from collections import Counter     # counts how often each word appears

import pandas as pd                 # working with tables (DataFrames)
import matplotlib.pyplot as plt     # static charts
import plotly.express as px         # interactive charts and maps

# Read the CSV file (it must be in the same folder as this script)
df = pd.read_csv("haunted_places.csv")

# Show the size of the table: (number of rows, number of columns)
print(df.shape)

# Preview the first 5 rows to understand the structure
df.head()

# %% [2] Top 10 states by number of haunted places
# Count how many haunted places each state has and keep the top 10
top_states = df["state"].value_counts().head(10)
print(top_states)

# Horizontal bar chart (sorted so the largest bar is on top)
top_states.sort_values().plot(kind="barh", color="darkorange", figsize=(8, 5))
plt.title("Top 10 States by Number of Haunted Places")
plt.xlabel("Number of places")
plt.tight_layout()
plt.savefig("top_states.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [3] Map of haunted hotspots
# Remove rows without coordinates
geo = df.dropna(subset=["latitude", "longitude"])

# Keep only points inside a reasonable US area (removes data entry errors)
geo = geo[geo["longitude"].between(-180, -60) & geo["latitude"].between(15, 72)]

# Scatter map of the USA: each dot is one haunted place
# This map type draws state borders itself, so it works inside VS Code
fig = px.scatter_geo(
    geo,
    lat="latitude",
    lon="longitude",
    hover_name="location",      # name shown when hovering over a point
    hover_data=["city", "state"],
    scope="usa",                # show only the USA
    opacity=0.4,                # semi-transparent dots, dense areas look darker
    title="Haunted Places in the USA",
)
fig.update_traces(marker=dict(size=4, color="darkorange"))
fig.update_layout(width=1000, height=600)   # make the map bigger
fig.show()

# %% [4] Most common words in descriptions
# Stop words are very common words that carry no meaning for our analysis
stop_words = set("""
a an the and or but if of to in on at by for with from as is was were be been
being are it its this that these those there their they them he she his her
him i you we our my me who whom which what when where why how not no so than
then too very can will would could should may might has have had do does did
said says one two also into out up down over about after before just all any
some more most other such only own same around back like still many
""".split())

# Combine all descriptions into one big lowercase text
text = " ".join(df["description"].dropna()).lower()

# Split the text into words (letters only, no numbers or punctuation)
words = re.findall(r"[a-z]+", text)

# Remove stop words and very short words (1-2 letters)
words = [w for w in words if w not in stop_words and len(w) > 2]

# Count each word and keep the 20 most frequent
top_words = pd.Series(Counter(words)).sort_values(ascending=False).head(20)
print(top_words)

# Horizontal bar chart of the top 20 words
top_words.sort_values().plot(kind="barh", color="purple", figsize=(8, 6))
plt.title("Top 20 Words in Haunted Place Descriptions")
plt.xlabel("Frequency")
plt.tight_layout()
plt.savefig("top_words.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [5] Ghost types: which kinds of ghosts are mentioned most often
# Each ghost type is defined by a search pattern (regular expression)
# \b means "word boundary", so "man" will not match "woman" or "manager"
ghost_types = {
    "woman / lady": r"\b(?:woman|lady|women)\b",
    "girl": r"\bgirls?\b",
    "boy": r"\bboys?\b",
    "child / children": r"\b(?:child|children|kids?)\b",
    "man": r"\b(?:man|men)\b",
    "soldier": r"\bsoldiers?\b",
    "nun / monk": r"\b(?:nuns?|monks?)\b",
    "shadow figure": r"\bshadow",
    "lady in white": r"\b(?:white lady|lady in white|woman in white)\b",
}

# Lowercase descriptions (empty text instead of missing values)
desc = df["description"].fillna("").str.lower()

# For each ghost type, count how many descriptions mention it
counts = {name: desc.str.contains(pattern, regex=True).sum()
          for name, pattern in ghost_types.items()}

ghosts = pd.Series(counts).sort_values()
print(ghosts)

# Bar chart of ghost types
ghosts.plot(kind="barh", color="black", figsize=(8, 5))
plt.title("Most Common Ghost Types in Descriptions")
plt.xlabel("Number of descriptions mentioning this type")
plt.tight_layout() 
plt.savefig("ghost_types.png", dpi=150, bbox_inches="tight")
plt.show()