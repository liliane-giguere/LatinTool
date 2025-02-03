# %%
import pandas as pd
import random 

columns = ["cat1", "cat2", "latin", "french", 'notes1', 'notes2', 'notes3','notes4']

df = pd.read_excel('latin_input_v4.xlsx', header=None, names=columns)
print("Bienvenue a l'outil d'apprentissage du latin!")
print()


# %%
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
    

# %%
df['Broad_Category'] = df['cat1'].apply(broad_category)
df['Specific_Category'] = df.apply(lambda row: specific_category(row['cat1'], row['cat2']), axis=1)


def choose_random_number(beg,end, already_chose):
    while True:
        num = random.randint(beg,end)
        if len(already_chose) == len(row_numbers):
            return print("Tu as fini de revoir tous les mots dans cette categorie!")
        if num not in already_chose:
            already_chose.append(num)
            return num
# %%

lang = int(input("1. latin -> francais ou 2. francais -> latin "))
print()

# %%
options = {}

for i, option in enumerate(df['Broad_Category'].unique(), 1):
    options[i] = option
    print(f"{i}. {option}")
print(f"6. Toutes categories")

choice = int(input('Quelle categorie de mot veux tu pratiquer? '))

if choice == 6:
    print('Tu as choisis le numero:', choice, "Toutes categories", end='\n')
else:
    print('Tu as choisis le numero:', choice, options[choice], end='\n')


# %%
specific = {}
if choice == 1:

    for i, specific_option in enumerate(df[df['cat1'] == 1]['Specific_Category'].unique(), 1):
        specific[i] = specific_option
    
    for i in range(1, 7):
        print(f"{i}. {specific[i]}")
    
    s_choice = int(input('Quelle categorie de verbes veux-tu pratiquer? ' ))
    print("Tu as choisis le numero:", s_choice, specific[s_choice], end='\n')

if choice == 2:
    for i, specific_option in enumerate(df[df['cat1'] == 2]['Specific_Category'].unique(), 1):
        specific[i] = specific_option
        print(f"{i}. {specific[i]}")
    
    s_choice = int(input('Quelle categorie de noms veux-tu pratiquer? ' ))
    print("Tu as choisis le numero:", s_choice, specific[s_choice], end='\n')


if choice == 3:
    for i, specific_option in enumerate(df[df['cat1'] == 3]['Specific_Category'].unique(), 1):
        specific[i] = specific_option
    
    for i in range(1, 3):
        print(f"{i}. {specific[i]}")
    
    s_choice = int(input('Quelle categorie d\'adjectifs veux-tu pratiquer?' ))
    print("Tu as choisis le numero:", s_choice, specific[s_choice], end='\n')


## verbes irreguliers avant verbes deponants

# %%
if choice <4:
    if choice == 3 and s_choice == 2:
        s_choice += 1
        filtered_df = df[(df["cat1"] == choice)]
        final_filtered_df = filtered_df[filtered_df["cat2"] == s_choice]
    else:
        filtered_df = df[df["cat1"] == choice]
        final_filtered_df = filtered_df[filtered_df["cat2"] == s_choice]
if choice == 6:
    final_filtered_df = df
else:
    final_filtered_df = df[(df["cat1"] == choice)]

# Get the row numbers of the matching words
row_numbers = final_filtered_df.index.tolist()
#print("Row numbers of matching words:", row_numbers)

# %%
rando = row_numbers
already_chose = []



# %%
while True: 
    if lang == 1:
        num = choose_random_number(row_numbers[0], row_numbers[-1], already_chose)
        word = final_filtered_df['latin'][num]
        answer = str(input(f'Quelle est la traduction de: {word} '))
        if answer == final_filtered_df['french'][num]:
            print('Correct!')
        else:
            print(final_filtered_df['french'][num])
            print('Incorrect!')
    else:
        num = choose_random_number(row_numbers[0], row_numbers[-1], already_chose)
        word = final_filtered_df['french'][num]
        answer = str(input(f'Quelle est la traduction de: {word} '))
        if answer == final_filtered_df['latin'][num]:
            print('Correct!')
        else:
            print(final_filtered_df['latin'][num])
            print('Incorrect!')


