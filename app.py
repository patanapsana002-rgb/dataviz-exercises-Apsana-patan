
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("video_games_sales.csv")

    # Remove missing years
    df = df.dropna(subset=["Year"])

    # Convert Year to integer
    df["Year"] = df["Year"].astype(int)

    return df


df = load_data()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎮 Video Game Sales Dashboard")

st.markdown(
    "### Exploring video game sales across platforms, genres, publishers and regions"
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🎛️ Dashboard Filters")

# Year filter
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Genre filter
genre_options = sorted(df["Genre"].dropna().unique())

selected_genres = st.sidebar.multiselect(
    "Select Genre",
    options=genre_options,
    default=genre_options
)

# Platform filter
platform_options = sorted(df["Platform"].dropna().unique())

selected_platforms = st.sidebar.multiselect(
    "Select Platform",
    options=platform_options,
    default=platform_options
)
# Publisher filter
publisher_options = sorted(
    df["Publisher"].dropna().unique()
)

selected_publishers = st.sidebar.multiselect(
    "Select Publisher",
    options=publisher_options,
    default=publisher_options
)
# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered_df = df[
    (df["Year"] >= year_range[0])
    & (df["Year"] <= year_range[1])
    & (df["Genre"].isin(selected_genres))
    & (df["Platform"].isin(selected_platforms))
    & (df["Publisher"].isin(selected_publishers))
]
# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("📊 Key Performance Indicators")

total_games = len(filtered_df)
total_sales = filtered_df["Global_Sales"].sum()
total_platforms = filtered_df["Platform"].nunique()
total_publishers = filtered_df["Publisher"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🎮 Games",
    f"{total_games:,}"
)

col2.metric(
    "🌎 Global Sales",
    f"{total_sales:,.2f} M"
)

col3.metric(
    "🕹️ Platforms",
    total_platforms
)

col4.metric(
    "🏢 Publishers",
    total_publishers
)
# --------------------------------------------------
# AUTOMATIC INSIGHTS
# --------------------------------------------------

st.subheader("💡 Key Insights")

if len(filtered_df) > 0:

    # Best platform
    best_platform = (
        filtered_df.groupby("Platform")["Global_Sales"]
        .sum()
        .idxmax()
    )

    best_platform_sales = (
        filtered_df.groupby("Platform")["Global_Sales"]
        .sum()
        .max()
    )

    # Best genre
    best_genre = (
        filtered_df.groupby("Genre")["Global_Sales"]
        .sum()
        .idxmax()
    )

    # Best publisher
    best_publisher = (
        filtered_df.groupby("Publisher")["Global_Sales"]
        .sum()
        .idxmax()
    )

    # Best region
    regional_totals = {
        "North America": filtered_df["NA_Sales"].sum(),
        "Europe": filtered_df["EU_Sales"].sum(),
        "Japan": filtered_df["JP_Sales"].sum(),
        "Other": filtered_df["Other_Sales"].sum()
    }

    best_region = max(
        regional_totals,
        key=regional_totals.get
    )

    insight1, insight2 = st.columns(2)

    with insight1:

        st.info(
            f"🎮 **Top Platform:** {best_platform} "
            f"generated approximately "
            f"**{best_platform_sales:,.2f} million** "
            f"in global sales."
        )

        st.info(
            f"🎯 **Top Genre:** "
            f"**{best_genre}** generated the highest "
            f"global sales among the selected genres."
        )

    with insight2:

        st.info(
            f"🏢 **Top Publisher:** "
            f"**{best_publisher}** generated the highest "
            f"global sales among the selected publishers."
        )

        st.info(
            f"🌍 **Leading Region:** "
            f"**{best_region}** recorded the highest "
            f"sales among the selected regions."
        )

else:

    st.warning(
        "No games match the selected filters. "
        "Please change your filters."
    )
# --------------------------------------------------
# SALES TREND
# --------------------------------------------------

st.subheader("📈 Global Video Game Sales Over Time")

year_sales = (
    filtered_df
    .groupby("Year")["Global_Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    year_sales,
    x="Year",
    y="Global_Sales",
    markers=True,
    title="Global Video Game Sales Over Time"
)

fig1.update_layout(
    xaxis_title="Year",
    yaxis_title="Global Sales (Millions)",
    template="plotly_white"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)
# --------------------------------------------------
# PLATFORM AND GENRE ANALYSIS
# --------------------------------------------------

col1, col2 = st.columns(2)

# Platform Performance
with col1:

    st.subheader("🎮 Platform Performance")

    platform_sales = (
        filtered_df
        .groupby("Platform")["Global_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        platform_sales,
        x="Global_Sales",
        y="Platform",
        orientation="h",
        title="Top 10 Platforms by Global Sales"
    )

    fig2.update_layout(
        xaxis_title="Global Sales (Millions)",
        yaxis_title="Platform",
        template="plotly_white",
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# Genre Performance
with col2:

    st.subheader("🎯 Genre Performance")

    genre_sales = (
        filtered_df
        .groupby("Genre")["Global_Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig3 = px.bar(
        genre_sales,
        x="Genre",
        y="Global_Sales",
        color="Genre",
        title="Global Sales by Genre"
    )

    fig3.update_layout(
        xaxis_title="Genre",
        yaxis_title="Global Sales (Millions)",
        template="plotly_white"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# --------------------------------------------------
# REGIONAL SALES AND TOP GAMES
# --------------------------------------------------

col1, col2 = st.columns(2)

# Regional Sales
with col1:

    st.subheader("🌍 Regional Sales")

    regional_sales = pd.DataFrame({
        "Region": [
            "North America",
            "Europe",
            "Japan",
            "Other"
        ],
        "Sales": [
            filtered_df["NA_Sales"].sum(),
            filtered_df["EU_Sales"].sum(),
            filtered_df["JP_Sales"].sum(),
            filtered_df["Other_Sales"].sum()
        ]
    })

    fig4 = px.bar(
        regional_sales,
        x="Region",
        y="Sales",
        title="Video Game Sales by Region"
    )

    fig4.update_layout(
        xaxis_title="Region",
        yaxis_title="Sales (Millions)",
        template="plotly_white"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )


# Top Games
with col2:

    st.subheader("🏆 Top 10 Best-Selling Games")

    top_games = (
        filtered_df
        .sort_values(
            "Global_Sales",
            ascending=False
        )
        .head(10)
    )

    fig5 = px.bar(
        top_games,
        x="Global_Sales",
        y="Name",
        orientation="h",
        color="Genre",
        title="Top 10 Games by Global Sales"
    )

    fig5.update_layout(
        xaxis_title="Global Sales (Millions)",
        yaxis_title="Game",
        template="plotly_white",
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )
# --------------------------------------------------
# GAME SEARCH
# --------------------------------------------------

st.subheader("🔎 Search for a Game")

search_game = st.text_input(
    "Enter a game name",
    placeholder="Example: Mario, FIFA, Pokemon..."
)

if search_game:

    search_results = filtered_df[
        filtered_df["Name"]
        .str.contains(
            search_game,
            case=False,
            na=False
        )
    ]

    if len(search_results) > 0:

        st.write(
            f"Found **{len(search_results)}** matching games."
        )

        st.dataframe(
            search_results[
                [
                    "Name",
                    "Platform",
                    "Year",
                    "Genre",
                    "Publisher",
                    "Global_Sales"
                ]
            ].sort_values(
                "Global_Sales",
                ascending=False
            ),
            use_container_width=True
        )

    else:

        st.warning(
            f"No games found matching **{search_game}**."
        )
# --------------------------------------------------
# DETAILED DATA
# --------------------------------------------------

with st.expander("📋 View Filtered Dataset"):

    st.write(
        f"Showing **{len(filtered_df):,}** games "
        "based on your selected filters."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )