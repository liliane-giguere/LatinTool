import streamlit as st

def main():
    st.title("Vocabulaire latin-francais")

    col1, col2 = st.columns([0.1,0.1])

    with col1:
        if st.button("Latin -> Francais"):
            st.write("Tu as choisis le Latin -> Francais")
    
    with col2:
        if st.button("Francais -> Latin"):
            st.write("Tu as choisis le Francais -> Latin")

    lang = st.radio("Choisissez la direction de traduction:", ("Latin -> Francais", "Francais -> Latin"))


unique_broad_categories = ['verbe', 'nom', 'adjectif', 'preposition', 'autre']
broad_category_choice = st.selectbox('Quelle catégorie de mot veux-tu pratiquer?', unique_broad_categories)
    # text_input = st.text_input("Enter Latin text:")
    # if text_input:
    #     st.write(f"You entered: {text_input}")

    # st.button("Submit")

if __name__ == "__main__":
    main()