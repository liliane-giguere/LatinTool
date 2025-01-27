import pandas as pd

columns = ["cat1", "cat2", "latin", "french"]
df = pd.read_excel('latin_input_v3.xlsx', header=None, names=columns)


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
    
def specific_category(cat1, cat2):
    if cat1 == 1:
        if cat2 == 1:
            return '1er groupe'
        elif cat2 == 2 or cat2 == 3 or cat2 == 4 :
            return cat2, 'eme groupe'
        elif cat2 == 4:
            return 'verbes irreguliers'
        else:
            return 'verbes deponants'
            
    elif cat2 == 2:
        return cat2, 'declinaison'
    
    elif cat1 == 3:
        if cat2 == 1:
            return '1ere & 2eme declinaison'
        else:
            return '3eme declinaison'
    
    else:
        return None

df['category'] = df['cat1'].apply(broad_category)
df['Specific_Category'] = df.apply(lambda row: specific_category(row['cat1'], row['cat2']), axis=1)

#options = {}

# for i, option in enumerate(df['category'].unique(), 1):
#     options[i] = option
#     print(f"{i}. {option}")

# choice = int(input('Quelle categorie de mot veux tu pratiquer?' ))

#print('Tu as choisis le numero', choice, options[choice])

# specific = {}
# if choice == 1:
#     for i, specific in enumerate(df[df['cat1'] == 1]['cat2'].unique(), 1):
#         specific[i] = specific
#         print(f"{i}. {specific}")
       




## groupe - verbe, declinaison -- 
## 5 irregulier, 6 deponant
