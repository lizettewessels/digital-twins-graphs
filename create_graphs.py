import json
import os

from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import seaborn as sns

from wordcloud import WordCloud

# Ensure the target directory exists
os.makedirs("./graphs", exist_ok=True)

# 1: Pie chart: Disciplines most prominent in digital twin research (combined data set)

# Load the JSON data from the file
with open("./data/processed/combined_data_set.json", "r") as file:
    data = json.load(file)

# Extracting discipline data from "annote" field
disciplines = {}
for entry in data:
    annote = entry.get("annote", "")
    discipline_part = annote.split("D: ")[-1] if "D: " in annote else None
    if discipline_part:
        discipline_list = discipline_part.split("; ")
        for discipline in discipline_list:
            if discipline in disciplines:
                disciplines[discipline] += 1
            else:
                disciplines[discipline] = 1

# Normalize the discipline names to have consistent capitalization and merge similar names
normalized_disciplines = {}
for key, value in disciplines.items():
    # Normalize capitalization
    normalized_key = " ".join(word.capitalize() for word in key.split())

    # Replace "And" with "and" in each normalized key
    normalized_key = normalized_key.replace("And", "and")

    # Define a mapping of similar discipline names
    merge_map = {
        "Sciences": "Science",
        "Engeneering": "Engineering",
        "Computer Science": "Computer Science",
        "Information Science": "Information Science",
        "Information Sciences": "Information Science",
        "Higher Education": "Higher Education",
        "Education": "Higher Education",
        "Social Sciences": "Social Science",
        "Research and Innovation": "Research and Development",
        "Research": "Research and Development",
        "Natural Sciences": "Natural Science",
        "Information Management": "Information Science",
        "Science and Technology": "Computer Science"
    }

    # Check if the normalized key should be merged with another key
    if normalized_key in merge_map:
        normalized_key = merge_map[normalized_key]

    if normalized_key in normalized_disciplines:
        normalized_disciplines[normalized_key] += value
    else:
        normalized_disciplines[normalized_key] = value

# Further normalization by merging specific disciplines under a common category
for merge in ["Internet and Technology Research", "Science and Technology", "Science", "Technology"]:
    if merge in normalized_disciplines:
        if "Science and Technology" in normalized_disciplines:
            normalized_disciplines["Science and Technology"] += normalized_disciplines[merge]
        else:
            normalized_disciplines["Science and Technology"] = normalized_disciplines[merge]
        del normalized_disciplines[merge]

# Sort the dictionary by values in descending order
normalized_disciplines = dict(sorted(normalized_disciplines.items(), key=lambda item: item[1], reverse=True))

# Setting Seaborn style
sns.set(style="whitegrid")

# Data for plotting
labels = list(normalized_disciplines.keys())
sizes = list(normalized_disciplines.values())

# Calculate total occurrences to find percentages
total = sum(sizes)

# Calculate percentages for each discipline
percentages = [f"{(size / total) * 100:.2f}%" for size in sizes]

# Create a bar chart with percentages shown next to each bar
plt.figure(figsize=(12, 8))
bars = sns.barplot(x=sizes, y=labels, palette="cubehelix", hue=labels, legend=False)
plt.xlabel("Number of Occurrences")
plt.ylabel("Disciplines")
plt.title("Bar Chart of Disciplines with Percentages")

# Add percentages next to the bars
for bar, percentage in zip(bars.patches, percentages):
    width = bar.get_width()
    plt.text(width + 0.3, bar.get_y() + bar.get_height()/2, f"{percentage}", va="center")

# Adjust the margins of the plot to prevent cutting off labels
plt.subplots_adjust(left=0.25)

# Save the figure with percentages
plt.savefig("./graphs/disciplines_bar_chart_with_percentages.png")
# plt.show()
plt.close()

# 2. Word Clouds: Author keywords most prominent in digital twin research (cr1, cr2, cr3 data sets)

# datasets = ["cr1_data_set.json", "cr2_data_set.json", "cr3_data_set.json"]
datasets = ["combined_data_set.json"]

# Define the new mapping based on similar concepts
concept_mapping = {
    "Digital Twin": ["DT", "Digital twin", "digital twin", "Digital Twin", "digital twins", "digital twins",
                     "Digital Twins", "digital twin", "DT uses", "Use cases of Digital Twin", "digital twin ecosystem",
                     "Levels of Digital Twin", "UNI-TWIN", "Digital Twin Maturity", "ZModel DT", "Digital twin.",
                     "Shop-floor Digital Twin", "virtual representation", "asset-administration shell",
                     "autonomous digital twin", "information fusion", "smart-manufacturing standard",
                     "Autonomous digital twin", "De-contextual communication"],
    "Metaverse": ["MV", "Metaverse", "metaverse", "Metaversity", "metaverse technologies", "metaverse learning",
                  "metaverse library", "metaversities"],
    "Artificial Intelligence": ["AI", "artificial intelligence", "Artificial intelligence", "Artificial Intelligence",
                                "artificial intelligence", "Artificial Intelligence (AI)"],
    "Virtual Reality": ["VR", "VR", "virtual reality", "Virtual reality", "virtual reality",
                        "augmented and virtual reality", "Extended reality", "mixed reality",
                        "Immersive virtual reality"],
    "Industry 4.0": ["Industry 4.0", "Industry 4.0", "4IR", "industry 4.0", "Fourth Industrial Revolution",
                     "Fourth Industrial Revolution"],
    "Information Sharing": ["IS", "information sharing", "information sharing"],
    "Augmented Reality": ["AR", "augmented reality", "Augmented reality", "Augmented Reality"],
    "Digital Learning": ["DL", "DL", "DL", "digital learning", "Digital Learning", "E-Learning", "online education",
                         "e-learning", "virtual education", "E-Learning", "metaverse learning", "E-Learning",
                         "online learning", "Digital education", "learning in the metaverse"],
    "Higher Education": ["HE", "HE", "higher education", "Higher education", "university education", "Higher Education",
                         "university", "university education", "Universities", "University 4.0",
                         "Teaching and Learning", "Teaching and Learning 4.0", "Teaching and learning",
                         "universities/colleges", "teachers", "students", "future of education", "learning process",
                         "Curriculum", "teaching and learning", "education", "Learning", "education.",
                         "Digital education", "Higher English Education", "edu-metaverse"],
    "Sustainability": ["Sustainability", "Sustainability", "sustainability", "Sustainable development",
                       "sustainability", "Sustainable smart manufacturing", "Sustainability", "Circular economy",
                       "Circular economy tools", "Digital economy", "Construction path", "Five-dimensional model",
                       "Sustainable development goals"],
    "Digital Ecosystem": ["Digital ecosystem", "digital business ecosystem", "Ecosystem", "Library 1.0", "Library 2.0",
                          "Library 3.0", "Library 4.0", "Library 5.0", "digital model", "digital shadows",
                          "Digital twin", "Digital ecosystem"],
    "Emerging Digital Technologies": ["Emerging digital technologies", "emerging technologies", "emerging technology",
                                      "Emerging Technologies", "Emerging Technologies", "Emerging Technologies",
                                      "Emerging Technologies", "Advanced technologies in libraries"],
    "Infrastructure": ["Infrastructure", "infrastructure"],
    "Metaversity": ["Metaversity", "Metaversity"],
    "Virtual Space": ["Virtual Space", "Virtual space"],
    "Industry 5.0": ["Industry 5.0", "Industry 5", "industry 5.0"],
    "Internet Of Things": ["Internet Of Things", "Internet of Things", "Internet of Things (IoT)", "Iot", "IoT",
                           "IoT applications"],
    "Privacy And Security": ["Privacy And Security", "Privacy", "Security and Privacy"],
    "Blockchain": ["Blockchain", "blockchain"],
    "Innovation": ["Innovation", "innovation"],
    "Mixed Reality": ["Mixed Reality", "Mixed Reality"],
    "Virtual Classroom": ["Virtual Classroom", "virtual classroom"],
    "Metaverse Technologies": ["Metaverse Technologies", "metaverse technologies"],
    "Digital Twin Ecosystem": ["Digital Twin Ecosystem", "digital twin ecosystem"],
    "Human-Computer Interaction": ["Human-Computer Interaction", "human computer interaction"],
    "Skills": ["Skills", "Skills", "skills"],
    "Big Data": ["Big Data", "big data", "Big data"],
    "Digital Age": ["Digital age", "Digital age"],
    "Digital Transformation": ["Digital Transformation", "Digital transformation"],
    "E-Learning": ["E-Learning", "E-Learning", "E-Learning", "E-Learning"],
    "Meta-Literacy": ["Meta-Literacy", "meta-literacy", "metaliteracy", "metaliteracy"],
    "User Interface": ["User Interface", "User Interface", "interface"],
    "Robotics": ["Robotics", "Robotics", "robotics"],
    "Cloud Computing": ["Cloud Computing", "cloud computing"],
    "Metaverse Learning": ["Metaverse Learning", "metaverse learning"],
    "Metaverse Libraries": ["Metaverse Libraries", "metaverse libraries"],
    "Virtual Libraries": ["Virtual Libraries", "Virtual libraries"],
    "Society 5.0": ["Society 5.0", "S5.0", "society 5.0"],
    "Digital Twinning": ["Digital Twinning", "digital twinning"],
    "Ethics": ["Ethics", "ethics"],
    "Machine Learning": ["Machine Learning", "Machine learning", "machine learning"]
}

for dataset in datasets:

    # Load JSON data from a file
    with open(f"./data/processed/{dataset}", "r") as file:
        data = json.load(file)
    
    # Initialize a Counter to keep track of keyword occurrences
    keyword_counts = Counter()
    
    # Loop through each entry in the JSON data
    for entry in data:
        # Get the keywords string and split it into a list of keywords
        keywords = entry.get("keywords", "").split(",")
        # Update the Counter with the keywords from this entry
        keyword_counts.update(keywords)

    # Initialize a new counter
    new_keyword_counts = Counter()

    # Map and sum values from the original counter based on the new mapping
    for new_key, old_keys in concept_mapping.items():
        sum_values = sum(keyword_counts[old_key] for old_key in old_keys)
        new_keyword_counts[new_key] = sum_values

    # Initialize the WordCloud object with adjusted parameters
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        max_words=200,
        max_font_size=450,
        scale=1,
        margin=1  # Reduce margin to decrease space between words
    )

    # Generate the word cloud using frequencies
    wordcloud.generate_from_frequencies(new_keyword_counts)

    # Create image name
    img_name = dataset.replace("_data_set.json", "")

    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")  # Turn off axis labels

    # Save the figure with percentages
    plt.savefig(f"./graphs/{img_name}_keyword_wordcloud.png")
    # plt.show()
    plt.close()

# 3. Geoplot: Countries most dominant in digital twin research (combined data set)

# Load JSON data from a file
with open("./data/processed/combined_data_set.json", "r") as file:
    data = json.load(file)

# Extracting countries data from "annote" field
countries = {}
for entry in data:
    annote = entry.get("annote", "")
    country_part = annote.split("C: ")[-1] if "C: " in annote else None
    if country_part:
        country_part = country_part.split("\nD: ")[0]
        country_list = country_part.split("; ")
        for country in country_list:
            if country in countries:
                countries[country] += 1
            else:
                countries[country] = 1

# Corrections to apply
# Correcting typographical errors
countries["Bahrain"] = countries.pop("Baghrain")
countries["Colombia"] = countries.pop("Columbia")
countries["Qatar"] = countries.pop("Quatar")

# Correcting and consolidating locations listed as cities or regions
countries["Iraq"] += countries.pop("Baghdad")
countries["United Arab Emirates"] += countries.pop("Dubai")
countries["UK"] += countries.pop("Scotland")
countries["South Korea"] = countries.pop("Korea")

# Create a DataFrame from your dictionary
data = {"Country": list(countries.keys()), "Articles": list(countries.values())}
df = pd.DataFrame(data)

# Load a map of the world
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Merge your data with the world map
world_df = world.merge(df, how="left", left_on="name", right_on="Country")

# Plotting the choropleth map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world_df.boundary.plot(ax=ax)
world_df.plot(column="Articles", ax=ax, legend=True,
              legend_kwds={"label": "Number of Articles on Digital Twins"},
              missing_kwds={"color": "lightgrey"})

# Save the choropleth map
plt.savefig("./graphs/choropleth_map_digital_twins.png")
plt.close()

# Plotting a bar chart for the top 10 countries
top_countries = df.nlargest(10, "Articles")
fig, bx = plt.subplots(figsize=(12, 8))
sns.barplot(x="Country", y="Articles", hue="Country", legend=False, data=top_countries, ax=bx, palette="viridis")
bx.set_title("Top 10 Countries by Digital Twins Research Articles")
bx.set_xlabel("Country")
bx.set_ylabel("Number of Articles")
plt.xticks(rotation=45)

# Save the bar chart
plt.savefig("./graphs/top_countries_digital_twins.png")
plt.close()

# 3. Barplot: Top contributing journals in digital twin research (combined data set)

# Load the data from the JSON file
with open("./data/processed/combined_data_set.json", "r") as file:
    data = json.load(file)

# Initialize a dictionary to count frequency of each journal
journal_counts = {}

# Iterate through each entry in the dataset
for entry in data:
    if "journal" in entry:
        journal = entry["journal"]
        if journal in journal_counts:
            journal_counts[journal] += 1
        else:
            journal_counts[journal] = 1

# Manual corrections for the journal counts
# Combining counts for specific journals

# Combining "Electronics" and "Electronics (Switzerland)"
journal_counts["Electronics"] = (
        journal_counts.get("Electronics", 0) + journal_counts.get("Electronics (Switzerland)", 0))
del journal_counts["Electronics (Switzerland)"]

# Combining "Sustainability" and "Sustainability (Switzerland)"
journal_counts["Sustainability"] = (
        journal_counts.get("Sustainability", 0) + journal_counts.get("Sustainability (Switzerland)", 0))
del journal_counts["Sustainability (Switzerland)"]

# Combining "Library Philosophy and Practice" and "Library Philosophy and Practice (e-journal)"
journal_counts["Library Philosophy and Practice"] = (
        journal_counts.get("Library Philosophy and Practice", 0) +
        journal_counts.get("Library Philosophy and Practice (e-journal)", 0))
del journal_counts["Library Philosophy and Practice (e-journal)"]

# Combining "Metaverse", "Journal of Metaverse", and "Metaverse Basic and Applied Research"
journal_counts["Metaverse"] = (
        journal_counts.get("Metaverse", 0) + journal_counts.get("Journal of Metaverse", 0) +
        journal_counts.get("Metaverse Basic and Applied Research", 0))
del journal_counts["Journal of Metaverse"]
del journal_counts["Metaverse Basic and Applied Research"]

# Extract the top 10 journals by frequency
top_journals = dict(sorted(journal_counts.items(), key=lambda item: item[1], reverse=True)[:10])

# Create a bar plot using seaborn
plt.figure(figsize=(12, 8))
sns.barplot(x=list(top_journals.values()), y=list(top_journals.keys()), hue=list(top_journals.keys()),
            palette="viridis", legend=False)
plt.title("Top 10 Journals by Frequency", fontsize=16)
plt.xlabel("Frequency", fontsize=14)
plt.ylabel("Journal", fontsize=14)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

# Save the plot to a file
plt.savefig("./graphs/top_10_journals.png")
plt.close()
