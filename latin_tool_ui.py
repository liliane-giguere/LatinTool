import streamlit as st
import pandas as pd
import random 

## Load functions
def broad_category(cat1):
    if cat1 == 1:
        return 'verbe'
    elif cat1 == 2:
        return 'nom'
    elif cat1 == 3:
        return 'adjectif'
    elif cat1 == 4:
        return 'preposition'
    else:
        return 'autre'
    
# %%
def specific_category(cat1, cat2):
    if cat1 == 1:
        if cat2 == 1:
            return '1er groupe'
        elif cat2 == 2 or cat2 == 3 or cat2 == 4 :
            return f"{cat2}eme groupe"
        elif cat2 == 5:
            return 'verbes irreguliers'
        elif cat2 == 6:
            return 'verbes deponants'
            
    elif cat1 == 2:
        if cat2 == 1:
            return '1ere declinaison'
        elif cat2 == 2 or cat2 == 3 or cat2 == 4 or cat2 == 5:
            return f"{cat2}eme declinaison"
    
    elif cat1 == 3:
        if cat2 == 1:
            return '1ere & 2eme declinaison'
        else:
            return '3eme declinaison'
    
    else:
        return None
    
def choose_random_number(beg,end, already_chose, row_numbers):
    while True:
        num = random.randint(beg,end)
        if len(already_chose) == len(row_numbers):
            return 999
        if num not in already_chose:
            already_chose.append(num)
            return num
    
## Load data
columns = ["cat1", "cat2", "latin", "french", 'notes1', 'notes2', 'notes3','notes4']

df = pd.read_excel('latin_input_v4.xlsx', header=None, names=columns)
df['Broad_Category'] = df['cat1'].apply(broad_category)
df['Specific_Category'] = df.apply(lambda row: specific_category(row['cat1'], row['cat2']), axis=1)

def main():
    st.title("Vocabulaire latin-francais")

     

    # Initialize session state
    if "selected_lang" not in st.session_state:
        st.session_state.selected_lang = None
    if "broad_category_choice" not in st.session_state:
        st.session_state.broad_category_choice = None
    if "already_chosen" not in st.session_state:
        st.session_state.already_chosen = []
    if 'random_word' not in st.session_state:
        st.session_state.random_word = None

    if st.session_state.selected_lang is None:
        if st.button("Latin -> Français", key="latin_to_french"):
            st.session_state.selected_lang = "latin_a_francais"
       
        if st.button("Français -> Latin", key="french_to_latin"):
            st.session_state.selected_lang = "francais_a_latin"
    
    if st.session_state.selected_lang:
        st.write(f"Langue selectionnee: **{st.session_state.selected_lang.replace('_', ' ')}**")

    # Reset button to allow re-selection
    if st.session_state.selected_lang:
        if st.button("Réinitialiser"):
            st.session_state.selected_lang = None
    
    unique_broad_categories = ['verbe', 'nom', 'adjectif', 'preposition', 'autre', 'toutes categories']
            
    if "selected_category" not in st.session_state or st.session_state.selected_category is None:
        st.session_state.selected_category = unique_broad_categories[0]

    selected_category = st.selectbox(
    'Quelle catégorie de mot veux-tu pratiquer?', 
    unique_broad_categories, 
    index=unique_broad_categories.index(st.session_state.selected_category) if st.session_state.selected_category else 0
    )
    
    if "selected_category" not in st.session_state or st.session_state.selected_category is None:
        st.session_state.selected_category = unique_broad_categories[0]

    if selected_category != st.session_state.selected_category:
        st.session_state.selected_category = selected_category
        st.write("Tu as choisis", st.session_state.selected_category)

    if selected_category in ('verbe', 'nom', 'adjectif'):
        if selected_category == 'verbe':
            unique_specific_cats = ['1er groupe', '2eme groupe', '3eme groupe', '4eme groupe', 'verbes irreguliers', 'verbes deponants', 'toutes categories']
            s_cat = st.selectbox('Quelle catégorie de verbe veux-tu pratiquer?', unique_specific_cats)
        if selected_category == 'nom':
            unique_specific_cats = ['1ere declinaison', '2eme declinaison', '3eme declinaison', '4eme declinaison', '5eme declinaison', 'toutes categories']
            s_cat = st.selectbox('Quelle catégorie de nom veux-tu pratiquer?', unique_specific_cats)
        if selected_category == 'adjectif':
            unique_specific_cats = ['1ere & 2eme declinaison', '3eme declinaison', 'toutes categories']
            s_cat = st.selectbox('Quelle catégorie d\'adjectif veux-tu pratiquer?', unique_specific_cats)

    filtered_df = df[(df['Broad_Category'] == selected_category) & (df['Specific_Category'] == s_cat)]
    row_numbers = filtered_df.index.tolist()

    if st.button('Générer un mot aléatoire') or st.button('Next'):
        random_row = choose_random_number(0, len(row_numbers) - 1, st.session_state.already_chosen, row_numbers=row_numbers)
        if random_row == 999:
            st.write("Tu as fini de revoir tous les mots dans cette categorie! Refresh la page pour recommencer")
        elif random_row is not None:
            st.session_state.random_word = filtered_df.iloc[random_row]
    

    if st.session_state.random_word is not None:
        if st.session_state.selected_lang == "latin_a_francais":
            question = st.session_state.random_word['latin']
            answer = st.session_state.random_word['french']
        else:
            question = st.session_state.random_word['french']
            answer = st.session_state.random_word['latin']

        st.write(f"Quelle est la traduction de {question}")
        user_answer = st.text_input("Votre réponse:")
        if st.button("Soumettre"):
            if user_answer.strip().lower() == answer.strip().lower():
                st.write("Correct!")
            else:
                st.write(f"Incorrect. La bonne réponse est: {answer}")

if __name__ == "__main__":
    main()