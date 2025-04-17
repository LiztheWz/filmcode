import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from collections import defaultdict

df = pd.read_csv("best_pic_nominees_winners.csv")

winners_df = df[df['Winner'] == True]
nominees_df = df[df['Winner'] == False]



page = st.sidebar.selectbox("Go to", ["Home", "Contact"])

if page == "Home":
    st.title("Welcome to my Film App!")

    st.write("In this website, you'll be able to explore the different features that influence whether or not a film wins the Academy Award for Best Picture.")
    st.write("Learn and have fun!")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Genre', 
                                                                'IMDb Rating & Runtime',
                                                                'Director', 
                                                                'Actors',
                                                                'Distributor',
                                                                'Box Office'])

    with tab1:
        st.write("How the Top 10 genres were distributed over the decades.")

        def genre_counts(df):
            exploded_category = df['Genre'].str.split(',').explode().str.strip()
            return exploded_category.value_counts()
        
        options = ["Drama", "Romance", "Comedy", "Biography", "Crime", "Adventure", "History", "War", "Thriller", "Action"]
        selection = st.segmented_control(
            "Genre", options, selection_mode="multi"
        )
        
        fig, ax = plt.subplots(figsize=(15, 8))

        if selection: 
            top_genres = genre_counts(df).head(10).index.tolist()

            genre_by_decade = {}

            for decade, group in df.groupby("Decade"):
                exploded = group['Genre'].dropna().str.split(',').explode().str.strip()
                filtered = exploded[exploded.isin(top_genres)]
                genre_counts_decade = Counter(filtered)
                genre_by_decade[decade] = genre_counts_decade

            genre_trend_df = pd.DataFrame(genre_by_decade).fillna(0).astype(int).T


            genre_trend_df[selection].plot(kind="line", ax=ax)

            ax.set_title("Top Genre Popularity by Decade")
            ax.set_ylabel("Number of Films")
            ax.set_xlabel("Decade")
            ax.set_xticks(range(len(genre_trend_df.index)))
            ax.set_xticklabels(genre_trend_df.index, rotation=45)
            ax.legend(title="Genre", loc='center left', bbox_to_anchor=(1, 0.5))
            plt.tight_layout()
            
            st.pyplot(fig)
        else:
            st.warning("Please select one or more genres to display the trend over time.")

        df = df.drop(columns='Decade')


        st.markdown("-------")

        st.write('Number of films per genre.')

        option_map = {
            0: "Winner",
            1: "Nominee",
            2: "All"
        }
        selection = st.segmented_control(
            "Category",
            options=option_map.keys(),
            format_func=lambda option: option_map[option],
            selection_mode="single",
        )

        if not selection:
            st.warning("Please select a category to display the chart.")
        else:
            selected_category = option_map[selection]


            genre_winners = genre_counts(winners_df)
            genre_nominees = genre_counts(nominees_df)

            genre_df = pd.DataFrame ({
                'Winners': genre_winners,
                'Nominees': genre_nominees
            })

            genre_df['Total'] = genre_df['Winners'] + genre_df['Nominees']
            genre_df = genre_df.sort_values(by='Total', ascending=False)




            fig, ax = plt.subplots(figsize=(15, 8))

            if selected_category == "Winner":
                genre_df['Winners'].plot(kind='bar', figsize=(12,6), color=['orange'], ax=ax)
                ax.set_title("Genre Counts of Winners")
            elif selected_category == "Nominee":
                genre_df['Nominees'].plot(kind='bar', figsize=(12,6), color=['orange'],ax=ax)
                ax.set_title("Genre Counts of Nominees")
            elif selected_category == "All":
                genre_df = genre_df.drop(columns='Total')
                genre_df.plot(kind='bar', figsize=(12,6), color=['orange', 'mediumseagreen'], ax=ax)
                ax.set_title("Genre Counts of All")

            
            ax.set_ylabel("Number of Films")
            ax.set_xlabel("Genre")
            ax.tick_params(axis='x', rotation=45)
                
            st.pyplot(fig)








    with tab2:
        st.write('The trend of IMDb ratings or runtimes over the years.')

        cat1 = st.radio(
            "Please select one.",
            ["IMDb Rating", "Runtime"],
            captions=[
                "What the films were rated on IMDb.com",
                "How long the films were.",
            ],
            key="trend_radio"
        )

        fig = plt.figure(figsize=(15, 8))

        if cat1 == "IMDb Rating":
            rating_by_decade = df.groupby("Year")["IMDbRating"].mean()
            sns.lineplot(data=rating_by_decade)
            plt.title("Average IMDb Rating by Year")
            plt.ylabel("Average Rating")


        if cat1 == "Runtime":
            runtime_by_decade = df.groupby("Year")["Runtime"].mean()
            sns.lineplot(data=runtime_by_decade)
            plt.title("Average Runtime by Year")
            plt.ylabel("Average Runtime (minutes)")
            

        plt.xlabel("Year")
        plt.tight_layout()
        st.pyplot(fig)


        st.markdown("------")
        st.write("The distribution of IMDb Ratings or Runtimes for all films.")

        cat2 = st.radio(
            "Please select one.",
            ["IMDb Rating", "Runtime"],
            captions=[
                "What the films were rated on IMDb.com",
                "How long the films were.",
            ],
            key="hist_radio"
        )

        fig2 = plt.figure(figsize=(15, 8))

        if cat2 == "IMDb Rating":
            sns.histplot(data=df, x='IMDbRating', hue='Winner', kde=True, bins=20)
            plt.title('Distribution of IMDb Ratings for Best Picture Winners vs Nominees')
            plt.xlabel('IMDb Rating')
            plt.ylabel('Frequency')


        if cat2 == "Runtime":
            sns.histplot(data=df, x='Runtime', hue='Winner', kde=True, bins=20)
            plt.title('Distribution of Runtimes for Best Picture Winners vs Nominees')
            plt.xlabel('Runtime (minutes)')
            plt.ylabel('Frequency')

        st.pyplot(fig2)







    with tab3:
        st.write('Information about films per director.')

        director_name = st.text_input('Enter the name of a director:')

        filtered_df = df[df['Director'].str.contains(director_name, case=False, na=False)]
        st.write(filtered_df)

        st.markdown("-----")
        st.write("The actors/actresses that worked the most with this director were:")

        def actor_director_combo(df, director_name, top_actors = 10):
            director_df = df[df['Director'].str.lower() == director_name.lower()]

            all_actors = []

            for actors in director_df['Actors']:
                actor = [a.strip() for a in actors.split(',')]
                all_actors.extend(actor)
    
            actor_counts = Counter(all_actors)
            return actor_counts.most_common(top_actors)
        
        top_actors = actor_director_combo(df, director_name, 10)
        for actor, count in top_actors:
            st.write(f"{actor}: {count} films")









    with tab4:
        st.write('Information about films per actor or actress.')

        actor_name = st.text_input('Enter the name of an actor or actress:')

        filtered_df = df[df['Actors'].str.contains(actor_name, case=False, na=False)]
        st.write(filtered_df)

        st.markdown("-----")
        st.write("Here you can explore the most frequent genres they've acted in.")

        def actor_genre_breakdown(df, actor_name, top_n=10):
            actor_df = df[df['Actors'].str.contains(actor_name, case=False, na=False)]

            all_genres = []

            for genres in actor_df['Genre'].dropna():
                genre_list = [g.strip() for g in genres.split(',')]
                all_genres.extend(genre_list)

            genre_counts = Counter(all_genres)
            return genre_counts.most_common(top_n)
        
        top_genres = actor_genre_breakdown(df, actor_name)

        for genre, count in top_genres:
            st.write(f"{genre}: {count} film(s)")






    with tab5:
        st.write('Distributing companies popular film genres.')

        option = st.selectbox(
            "Which distributors would you like to explore?",
            ["Paramount Pictures", "Columbia Pictures", "United Artists", "Warner Bros. Pictures",
             "Universal Pictures", "20th Century Fox", "Fox Searchlight Pictures", "Orion Pictures"],
        )

        def get_genres_for_distributor(df, distributor):
            genre_list = []

            filtered = df[df['Distributor'] == distributor]
            for genres in filtered['Genre'].dropna():
                genre_list.extend([g.strip() for g in genres.split(',')])

            return genre_list

        distributor_genres = get_genres_for_distributor(df, option)

        genre_counts = pd.Series(distributor_genres).value_counts()

        st.write(f"Genres distributed by **{option}**:")
        st.dataframe(genre_counts.reset_index().rename(columns={'index': 'Genre', 0: 'Count'}))

        st.write("Genre distribution:")
        fig, ax = plt.subplots(figsize=(10, 6))
        genre_counts.plot(kind='bar', color='mediumseagreen', ax=ax)
        ax.set_title(f"Genres Distributed by {option}")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Number of Films")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        







    with tab6:
        st.write('Box Office earnings over the years.')
        boxoffice_by_year = df.groupby("Year")["BoxOffice"].mean()

        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(data=boxoffice_by_year)
        plt.title("Average Box Office by Year")
        plt.ylabel("Average Box Office")
        plt.xlabel("Year")
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("-----")

        st.write('Top Box Office earnings per decade.')

        def top_grossing_decade(df):
            df = df.copy()

            if 'Decade' not in df.columns:
                df['Decade'] = (df['Year'] // 10) * 10

            df = df.dropna(subset=['BoxOffice'])
            df_sorted = df.sort_values(by='BoxOffice', ascending=False)
            top_per_decade = df_sorted.groupby('Decade').first().reset_index()
            return top_per_decade[['Decade', 'Movie', 'Year', 'BoxOffice']]
            
        top_grossing = top_grossing_decade(df)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_grossing, x='Decade', y='BoxOffice', hue='Movie', dodge=False)
        ax.set_title("Highest Grossing Films by Decade")
        ax.set_ylabel("Box Office ($)")
        st.pyplot(fig)

        
        
        










elif page == "Contact":
    st.title("Contact Page")
    st.write("Feel free to reach out to me if you have any questions, concerns, or curiosities!")
    st.write("")
    st.write("")


    st.markdown("[Visit LinkedIn Page](www.linkedin.com/in/liz-mendoza-a6382b214)")
    st.markdown("[📧 E-mail](mailto:lizethm3@byu.edu)")





