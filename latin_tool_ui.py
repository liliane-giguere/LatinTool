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
     
    # Initialize session state variables
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "selected_lang" not in st.session_state:
        st.session_state.selected_lang = None
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "selected_specific_category" not in st.session_state:
        st.session_state.selected_specific_category = None
    if "already_chosen" not in st.session_state:
        st.session_state.already_chosen = []
    if 'random_word' not in st.session_state:
        st.session_state.random_word = None

    # Screen 1: Language Selection
    if st.session_state.step == 1:
        st.header("Étape 1: Choisir la direction de traduction")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Latin → Français"):
                st.session_state.selected_lang = "latin_a_francais"
                st.session_state.step = 2
        with col2:
            if st.button("Français → Latin"):
                st.session_state.selected_lang = "francais_a_latin"
                st.session_state.step = 2

    # Screen 2: Broad Category Selection
    elif st.session_state.step == 2:
        st.header("Étape 2: Choisir la catégorie")
        st.write(f"Direction de traduction: **{st.session_state.selected_lang.replace('_', ' ')}**")
        
        unique_broad_categories = ['verbe', 'nom', 'adjectif', 'preposition', 'autre', 'toutes categories']
        selected_category = st.selectbox(
            'Quelle catégorie de mot veux-tu pratiquer?', 
            unique_broad_categories
        )
        
        if st.button("Suivant"):
            st.session_state.selected_category = selected_category
            st.session_state.step = 3

    # Screen 3: Specific Category Selection
    elif st.session_state.step == 3:
        st.header("Étape 3: Choisir la sous-catégorie")
        st.write(f"Direction de traduction: **{st.session_state.selected_lang.replace('_', ' ')}**")
        st.write(f"Catégorie: **{st.session_state.selected_category}**")

        if st.session_state.selected_category == 'verbe':
            unique_specific_cats = ['1er groupe', '2eme groupe', '3eme groupe', '4eme groupe', 
                                  'verbes irreguliers', 'verbes deponants', 'toutes categories']
            label = 'Quelle catégorie de verbe veux-tu pratiquer?'
        elif st.session_state.selected_category == 'nom':
            unique_specific_cats = ['1ere declinaison', '2eme declinaison', '3eme declinaison', 
                                  '4eme declinaison', '5eme declinaison', 'toutes categories']
            label = 'Quelle catégorie de nom veux-tu pratiquer?'
        elif st.session_state.selected_category == 'adjectif':
            unique_specific_cats = ['1ere & 2eme declinaison', '3eme declinaison', 'toutes categories']
            label = 'Quelle catégorie d\'adjectif veux-tu pratiquer?'
        else:
            st.session_state.step = 4
            st.rerun()

        selected_specific = st.selectbox(label, unique_specific_cats)
        
        if st.button("Commencer l'exercice"):
            st.session_state.selected_specific_category = selected_specific
            st.session_state.step = 4

    # Screen 4: Practice
    elif st.session_state.step == 4:
        st.header("Exercice de vocabulaire")
        st.write(f"Direction de traduction: **{st.session_state.selected_lang.replace('_', ' ')}**")
        st.write(f"Catégorie: **{st.session_state.selected_category}**")
        if hasattr(st.session_state, 'selected_specific_category'):
            st.write(f"Sous-catégorie: **{st.session_state.selected_specific_category}**")

        # Filter dataframe based on selections
        if st.session_state.selected_category != 'toutes categories':
            if hasattr(st.session_state, 'selected_specific_category') and st.session_state.selected_specific_category != 'toutes categories':
                filtered_df = df[
                    (df['Broad_Category'] == st.session_state.selected_category) & 
                    (df['Specific_Category'] == st.session_state.selected_specific_category)
                ]
            else:
                filtered_df = df[df['Broad_Category'] == st.session_state.selected_category]
        else:
            filtered_df = df

        row_numbers = filtered_df.index.tolist()

        if st.button('Générer un mot aléatoire') or st.button('Suivant'):
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

            st.write(f"Quelle est la traduction de: **{question}**")
            user_answer = st.text_input("Votre réponse:")
            if st.button("Soumettre"):
                if user_answer.strip().lower() == answer.strip().lower():
                    st.success("Correct! ✨")
                else:
                    st.error(f"Incorrect. La bonne réponse est: {answer}")

    # Add a reset button on all screens except the first
    if st.session_state.step > 1:
        if st.button("Recommencer"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()