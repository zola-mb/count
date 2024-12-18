#Import steps here
    #Import libraries
    #Import data
    #Run calculations
    #Create graphs
    #Visualise on streamlit

#Import libraries
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from PIL import Image

#Landing page
st.set_page_config(page_title="FMSP Analysis", page_icon=":child:", layout="centered")
st.title("FMSP Analysis")
img_contact_form = Image.open("COUNT Africa - Play Day - 04 October 2024 (23).jpg")
st.image(img_contact_form, use_column_width=True)

import streamlit as st

# Define credentials
credentials = {
    'count': 'fmsp'
}

# Login function
def login():
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Check if user is logged in
    if st.session_state.user:
        st.sidebar.success(f"Logged in as {st.session_state.user}")
        return True
    else:
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username", key="username")
        password = st.sidebar.text_input("Password", type="password", key="password")

        if st.sidebar.button("Login"):
            if username in credentials and credentials[username] == password:
                st.session_state.user = username
                st.sidebar.success(f"Logged in as {username}")
                st.experimental_rerun()
            else:
                st.sidebar.error("Incorrect username or password")
        return False

# Main app logic
if login():
    # Protected content
    st.write("Welcome to the FMSP analysis data portal.")

    st.write("---")

    #import data
    count = pd.read_excel("2024 Combined - Count Assessments (2).xlsx")
    report = pd.read_excel("FMSP Facilitator Data Collection (Responses).xlsx")
    masshours = pd.read_excel("Count Total Hours.xlsx")

    #Run calculations
    
    #Sessions
    
    st.header("Sessions Data")
    st.write("Children across 13 centres received a total number of 2 492 Maths and Sciences sessions from February to "
             "November. The two charts below show a) total number of sessions done at each ECD Centre and; b) total "
             "number of sessions done per month.")
    
    report["Sessions"] = pd.to_numeric(report["Sessions"], errors="coerce")
    
    report = report.dropna(subset=["Sessions"])
    
    report["Sessions"] = report["Sessions"].fillna(0)
    
    sessions = report[["ECDC Name", "Sessions", "Month"]].reset_index()
    sessions = sessions.sort_values(by="Sessions", ascending=False, na_position='last').reset_index()
    
    fig_sessions = px.histogram(sessions, x="ECDC Name", y="Sessions", color="ECDC Name",title="Total Sessions Done per ECDC")
    #fig_sessions.show()
    st.plotly_chart(fig_sessions)
    
    # Define the proper order of months
    month_order = [
        "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November"
    ]
    
    # Convert the Month column to a categorical type with the specified order
    sessions["Month"] = pd.Categorical(sessions["Month"], categories=month_order, ordered=True)
    
    # Sort by Month
    sessions = sessions.sort_values("Month")
    
    # Plot the updated data
    fig_monthlysessions = px.histogram(sessions, x="Month", y="Sessions", color="Month", title="Total Sessions Done per Month")
    #fig_sessions.show()
    st.plotly_chart(fig_monthlysessions)
    sessions
    
    st.write("---")
    
    #Youth Hours
    st.subheader("Youth Hours")
    st.write("Youth dedicated a total of 9 184 hours throughout the year, running FMSP sessions, Siyadlala workshops and helping out in their respective ECD Centres.")
    total_hours = masshours[["Full Name", "Total Hours"]].sort_values(by="Total Hours", ascending=False).reset_index()
    px.histogram(total_hours, x="Full Name", y="Total Hours", color="Full Name")
    fig_hours = px.histogram(total_hours, x="Full Name", y="Total Hours", color="Full Name")
    st.plotly_chart(fig_hours)
    total_hours
    
    st.write("---")
    
    #Save columns in a Series
    column_numeric = ["Nov - Oral Counting (10)", "Nov - One to One Counting (10)", "Nov - Matching (5)", "Nov - Sorting & Reasoning (2)", "Nov - Measuring (4)", "Nov - Floating vs Sinking (8)", "Nov - Animals (20)", "Nov - Clothes (8)", "Nov - Feely Bags (4)", "Nov - Total (71)"]
    
    # List of columns to convert
    column_numeric = [
        "Nov - Oral Counting (10)",
        "Nov - One to One Counting (10)",
        "Nov - Matching (5)",
        "Nov - Sorting & Reasoning (2)",
        "Nov - Measuring (4)",
        "Nov - Floating vs Sinking (8)",
        "Nov - Animals (20)",
        "Nov - Clothes (8)",
        "Nov - Feely Bags (4)",
        "Nov - Total (71)"
    ]
    
    # Convert each column in the list to numeric
    for col in column_numeric:
        count[col] = pd.to_numeric(count[col], errors='coerce')
    
    # Convert specified columns to int64
    for col in column_numeric:
        # Convert to numeric, coercing invalid values to NaN
        count[col] = pd.to_numeric(count[col], errors='coerce')
        # Fill NaN with a default value (e.g., 0) or handle as needed
        count[col] = count[col].fillna(0).astype('int64')
    
    #Top Performing Children
    st.header("Top Performing Children")
    
    #Baseline
    baseline_results = count[["Full Name", "School", "Jan - Total (71)"]].sort_values(by="Jan - Total (71)", ascending=False).head(10)
    #baseline_results
    fig_baseline = px.histogram(baseline_results, x="Full Name", y="Jan - Total (71)", color="School", title="Top 10 Performing Children (Baseline)")
    #fig.show()
    st.plotly_chart(fig_baseline)
    baseline_results
    
    #Endline
    endline_results = count[["Full Name", "School", "Nov - Total (71)"]].sort_values(by="Nov - Total (71)", ascending=False).head(10)
    #endline_results
    fig_endline = px.histogram(endline_results, x="Full Name", y="Nov - Total (71)", color="School", title="Top 10 Performing Children (Endline)")
    #fig.show
    st.plotly_chart(fig_endline)
    endline_results
    
    st.write("---")
    
    st.header("Analysis on Baseline vs Endline Results")
    
    #Section - Overall Improvement
    
    st.subheader("Overall Improvement")
    st.write("This is overall improvement for the entire assessment across the different the different ECDCs. This is based on scores on Baseline vs Endline. Six of the nine centres showed improvement.")
    
    count["Overall Improvement"] = count["Nov - Total (71)"] - count["Jan - Total (71)"]
    
    # Sort the DataFrame based on the "Overall Improvement" column in descending order
    count_sorted = count.sort_values(by="Overall Improvement", ascending=False)
    #count_sorted.columns
    
    overall_improvement = count_sorted.groupby("School")["Overall Improvement"].mean().sort_values(ascending=False).reset_index()
    
    #Visualise Overall Improvement
    
    fig_overall = px.bar(overall_improvement, x="School", y="Overall Improvement", color="School",title="Overall Improvement by School")
    #fig.show()
    st.plotly_chart(fig_overall)
    
    #Oral Counting Improvement
    st.subheader("Oral Counting Improvement")
    st.write("This is average improvement for the Oral Counting question. Eight centres showed improvement, with Avumile showing zero improvement.")
    
    count["Improvement - Oral Counting"] = count["Nov - Oral Counting (10)"] - count["Jan - Oral Counting (10)"]
    
    # Sort the DataFrame based on the "Overall Improvement" column in descending order
    count_sorted = count.sort_values(by="Overall Improvement", ascending=False)
    
    df_count = count_sorted[['School', 'Jan - Oral Counting (10)', 'Jan - One to One Counting (10)',
           'Jan - Matching (5)', 'Jan - Sorting & Reasoning (2)',
           'Jan - Measuring (4)', 'Jan - Floating vs Sinking (8)',
           'Jan - Animals (20)', 'Jan - Clothes (8)', 'Jan - Feely Bags (4)',
           'Jan - Total (71)', 'Nov - Oral Counting (10)',
           'Nov - One to One Counting (10)', 'Nov - Matching (5)',
           'Nov - Sorting & Reasoning (2)', 'Nov - Measuring (4)',
           'Nov - Floating vs Sinking (8)', 'Nov - Animals (20)',
           'Nov - Clothes (8)', 'Nov - Feely Bags (4)', 'Nov - Total (71)', 'Overall Improvement']]
    
    oral_improvement = count_sorted[["School","Jan - Oral Counting (10)","Nov - Oral Counting (10)", "Improvement - Oral Counting"]]
    oral_improvement.head(15).sort_values(by="Improvement - Oral Counting",ascending=False).reset_index()
    
    mean_oral = oral_improvement.groupby("School")["Improvement - Oral Counting"].mean().reset_index()
    #mean_oral
    fig_oral = mean_oral.sort_values(by="Improvement - Oral Counting",ascending=False).reset_index()
    #fig_oral
    fig_oralchart = px.histogram(fig_oral, x="School", y="Improvement - Oral Counting",color="School", title="Oral Improvement by School")
    #fig.show()
    st.plotly_chart(fig_oralchart)
    
    #1-1 Counting Improvement
    st.subheader("1-1 Counting Improvement")
    st.write("This is improvement for the 1-1 Counting question. Six out of nine centres showed improvement.")
    
    count_sorted["Improvement - Counting"] = count_sorted["Nov - One to One Counting (10)"] - count["Jan - One to One Counting (10)"]
    count_improvement = count_sorted[["School", "Jan - One to One Counting (10)","Nov - One to One Counting (10)","Improvement - Counting"]]
    count_improvement.head(15).sort_values(by="Improvement - Counting",ascending=False).reset_index()
    mean_counting = count_improvement.groupby("School")["Improvement - Counting"].mean().reset_index()
    #mean_counting
    fig_counting = mean_counting.sort_values(by="Improvement - Counting", ascending=False)
    #fig_counting
    fig_countingchart = px.histogram(fig_counting, x="School", y="Improvement - Counting",color="School", title="Counting Improvement by School")
    #fig.show()
    st.plotly_chart(fig_countingchart)
    
    #Matching Improvement
    st.subheader("Matching Improvement")
    st.write("Most children across the nine centres scored lower than their baseline scores on this question. It is worth noting that children from Avumile, which joined the programme much later, showed the most improvement.")
    
    count_sorted["Improvement - Matching"] = count_sorted["Nov - Matching (5)"] - count["Jan - Matching (5)"]
    match_improvement = count_sorted[["School","Jan - Matching (5)","Nov - Matching (5)", "Improvement - Matching"]]
    match_improvement.head(15).sort_values(by="Improvement - Matching",ascending=False).reset_index()
    mean_matching = match_improvement.groupby("School")["Improvement - Matching"].mean().reset_index()
    fig_matching = mean_matching.sort_values(by="Improvement - Matching", ascending=False)
    fig_match = px.histogram(fig_matching, x="School", y="Improvement - Matching",color="School", title="Matching Improvement by School")
    #fig.show()
    st.plotly_chart(fig_match)
    
    #Sorting & Reasoning Improvement
    st.subheader("Sorting & Reasoning Improvement")
    st.write("The children at Siyabulela recorded the most improvement, with majority from other centres not showing much improvement.")
    
    count_sorted["Improvement - Sorting & Reasoning"] = count_sorted["Nov - Sorting & Reasoning (2)"] - count["Jan - Sorting & Reasoning (2)"]
    sort_improvement = count_sorted[["School","Jan - Sorting & Reasoning (2)","Nov - Sorting & Reasoning (2)", "Improvement - Sorting & Reasoning"]]
    sort_improvement.head(15).sort_values(by="Improvement - Sorting & Reasoning", ascending=False).reset_index()
    sort_mean = sort_improvement.groupby("School")["Improvement - Sorting & Reasoning"].mean().reset_index()
    #sort_mean
    fig_sort = sort_mean.sort_values(by="Improvement - Sorting & Reasoning",ascending=False).reset_index()
    fig_sorting = px.histogram(fig_sort, x="School", y="Improvement - Sorting & Reasoning",color="School", title="Sorting & Reasoning Improvement by School")
    #fig.show()
    st.plotly_chart(fig_sorting)
    
    #Measuring Improvement
    st.subheader("Measuring Improvement")
    st.write("Four of nine ECD Centres showed improvement. Again, it is interesting to note that the centres that joined later in the year and with less programmes make up the list of improved centres.")
    
    count_sorted["Improvement - Measuring"] = count_sorted["Nov - Measuring (4)"] - count["Jan - Measuring (4)"]
    measuring_improvement = count_sorted[["School","Jan - Measuring (4)","Nov - Measuring (4)", "Improvement - Measuring"]]
    measuring_improvement.head(15).sort_values(by="Improvement - Measuring",ascending=False).reset_index()
    mean_measuring = measuring_improvement.groupby("School")["Improvement - Measuring"].mean().reset_index()
    #mean_measuring
    fig_measuring = mean_measuring.sort_values(by="Improvement - Measuring", ascending=False).reset_index()
    fig_measure = px.histogram(fig_measuring, x="School", y="Improvement - Measuring",color="School", title="Measuring Improvement by School")
    #fig.show()
    st.plotly_chart(fig_measure)
    
    #Floating vs Sinking Improvement
    st.subheader("Floating vs Sinking Improvement")
    st.write("Six out of nine centres improved. Avumile and St. Mary also joined late in the year and do not have a lot of programmes running.")
    
    count_sorted["Improvement - Floating vs Sinking"] = count_sorted["Nov - Floating vs Sinking (8)"] - count["Jan - Floating vs Sinking (8)"]
    float_improvement = count_sorted[["School","Jan - Floating vs Sinking (8)","Nov - Floating vs Sinking (8)", "Improvement - Floating vs Sinking"]]
    float_improvement.head(15).sort_values(by="Improvement - Floating vs Sinking", ascending=False).reset_index()
    mean_float = float_improvement.groupby("School")["Improvement - Floating vs Sinking"].mean().reset_index()
    #mean_float
    fig_float = mean_float.sort_values(by="Improvement - Floating vs Sinking", ascending=False).reset_index()
    fig_floating = px.histogram(fig_float, x="School", y="Improvement - Floating vs Sinking",color="School", title="Floating vs Sinking Improvement by School")
    #fig.show
    st.plotly_chart(fig_floating)
    
    
    #Animals Improvement
    st.subheader("Animals Improvement")
    st.write("Children across all nine centres improved on this question.")
    
    count_sorted["Improvement - Animals"] = count_sorted["Nov - Animals (20)"] - count["Jan - Animals (20)"]
    animals_improvement = count_sorted[["School","Jan - Animals (20)","Nov - Animals (20)", "Improvement - Animals"]]
    animals_improvement.head(15).sort_values(by="Improvement - Animals", ascending=False).reset_index()
    mean_animals = animals_improvement.groupby("School")["Improvement - Animals"].mean().reset_index()
    #mean_animals
    fig_animals = mean_animals.sort_values(by="Improvement - Animals", ascending=False).reset_index()
    fig_animalschart = px.histogram(fig_animals, x="School", y="Improvement - Animals",color="School", title="Animals Improvement by School")
    #fig.show
    st.plotly_chart(fig_animalschart)
    
    #Clothes Improvement
    st.subheader("Clothes Improvement")
    st.write("Children from six out of nine centres could differentiate between summer and winter clothes.")
    
    count_sorted["Improvement - Clothes"] = count_sorted["Nov - Clothes (8)"] - count["Jan - Clothes (8)"]
    clothes_improvement = count_sorted[["School", "Jan - Clothes (8)", "Nov - Clothes (8)", "Improvement - Clothes"]]
    clothes_improvement.head(15).sort_values(by="Improvement - Clothes", ascending=False).reset_index()
    mean_clothes = clothes_improvement.groupby("School")["Improvement - Clothes"].mean().reset_index()
    #mean_clothes
    fig_clothes = mean_clothes.sort_values(by="Improvement - Clothes", ascending=False).reset_index()
    fig_clotheschart = px.histogram(fig_clothes, x="School", y="Improvement - Clothes",color="School", title="Clothes Improvement by School")
    #fig.show
    st.plotly_chart(fig_clotheschart)
    
    #Feely Bags
    st.subheader("Feely Bags Improvement")
    st.write("Five out of nine centres improved, with Avumile leading here again.")
    
    count_sorted["Improvement - Feely Bags"] = count_sorted["Nov - Feely Bags (4)"] - count["Jan - Feely Bags (4)"]
    bags_improvement = count_sorted[["School", "Jan - Feely Bags (4)", "Nov - Feely Bags (4)", "Improvement - Feely Bags"]]
    bags_improvement.head(15).sort_values(by="Improvement - Feely Bags", ascending=False).reset_index()
    mean_bags = bags_improvement.groupby("School")["Improvement - Feely Bags"].mean().reset_index()
    #mean_bags
    fig_bags = mean_bags.sort_values(by="Improvement - Feely Bags", ascending=False).reset_index()
    fig_feelybags = px.histogram(fig_bags, x="School", y="Improvement - Feely Bags",color="School", title="Feely Bags Improvement by School")
    #fig.show()
    st.plotly_chart(fig_feelybags)
    
    st.write("---")
    
    #Stats on Gender and Performance
    st.header("Stats on Gender and Performance")
    st.subheader("Gender breakdown")
    st.write("Breakdown of gender for children who were present in both baseline and endline assessments.")
    
    gender = count[["School", "Gender", "Nov - Total (71)", "Jan - Total (71)", "Overall Improvement"]].sort_values(by="Overall Improvement", ascending=False).reset_index()
    gender_stats = gender.Gender.value_counts().reset_index()
    gender_stats = gender.Gender.value_counts()
    plot_gender = px.pie(
        gender_stats,
        names=gender_stats.index,
        values=gender_stats.values,
    )
    st.plotly_chart(plot_gender)
    gender_stats
    
    st.subheader("Gender Performance")
    st.write("Analysis of performance differences between boys and girls who participated in both the baseline and endline assessments. The chart below shows that amongst the children that improved, 54% of them were girls.")
    gender["Improved Only"] = (gender["Overall Improvement"] >= 0).astype(int)
    gender["Improved Only"].value_counts().reset_index()
    improved = gender[["Gender", "Improved Only"]]
    fig_improved = px.pie(improved, names="Gender", values="Improved Only")
    st.plotly_chart(fig_improved)

else:
    # Message for non-logged-in users
    st.write("You need to log in to view this content.")
