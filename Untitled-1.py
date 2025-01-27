# %%
import pandas as pd
import random 

columns = ["cat1", "cat2", "latin", "french", 'notes1', 'notes2', 'notes3','notes4']

df = pd.read_excel('latin_input_v4.xlsx', header=None, names=columns)


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
        elif cat2 == 4:
            return 'verbes irregulier'
        else:
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

# %%
lang = int(input("1. latin -> francais ou 2. francais -> latin "))

# %%
options = {}

for i, option in enumerate(df['Broad_Category'].unique(), 1):
    options[i] = option
    print(f"{i}. {option}")


choice = int(input('Quelle categorie de mot veux tu pratiquer?' ))

print('Tu as choisis le numero:', choice, options[choice])


# %%
specific = {}
if choice == 1:

    for i, specific_option in enumerate(df[df['cat1'] == 1]['Specific_Category'].unique(), 1):
        specific[i] = specific_option
    
    for i in range(1, 6):
        print(f"{i}. {specific[i]}")
    
    s_choice = int(input('Quelle categorie de verbes veux-tu pratiquer?' ))

if choice == 2:
    for i, specific_option in enumerate(df[df['cat1'] == 2]['Specific_Category'].unique(), 1):
        specific[i] = specific_option
    
    for i in (0,2):
        print(f"{i}. {specific[i]}")
    
    s_choice = int(input('Quelle categorie de noms veux-tu pratiquer?' ))

if choice == 3:
    for i, specific_option in enumerate(df[df['cat1'] == 3]['Specific_Category'].unique(), 1):
        specific[i] = specific_option
    
    for i in range(1, 3):
        print(f"{i}. {specific[i]}")
    
    s_choice = int(input('Quelle categorie d\'adjectifs veux-tu pratiquer?' ))

## verbes irreguliers avant verbes deponants

# %%
if choice <4:
    if choice == 3 and s_choice == 2:
        s_choice += 1
        filtered_df = df[(df["cat1"] == choice) & (df["cat2"] == 1)]
    else:
        filtered_df = df[(df["cat1"] == choice) & (df["cat2"] == s_choice)]
else:
    filtered_df = df[(df["cat1"] == choice)]

# Get the row numbers of the matching words
row_numbers = filtered_df.index.tolist()
#print("Row numbers of matching words:", row_numbers)

# %%
def choose_random_number(beg,end):
    return random.randint(beg,end)


# %%
rando = row_numbers
already_chose = []
num = choose_random_number(row_numbers[0], row_numbers[-1])
if num in already_chose:
   num = choose_random_number(row_numbers[0], row_numbers[-1]) 
   already_chose.appentd(num)


# %%
if lang == 1:
    num = choose_random_number(row_numbers[0], row_numbers[-1])
    word = filtered_df['latin'][num]
    answer = str(input(f'Quelle est la traduction de: {word}'))
    if answer == filtered_df['french'][num]:
        print(filtered_df['french'][num])
        print('Correct!')
    else:
        print(filtered_df['french'][choose_random_number(row_numbers[0], row_numbers[-1])])
        print('Incorrect!')
else:
    word = filtered_df['french'][choose_random_number(row_numbers[0], row_numbers[-1])]
    answer = str(input(f'Quelle est la traduction de: {word}'))


