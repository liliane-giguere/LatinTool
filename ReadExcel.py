import pandas as pd


columns = ["cat1", "cat2", "latin", "french"]
df = pd.read_excel('latin_input_v2.xlsx', header=None, names=columns)

def broad_category(cat1):
    if cat1 == 1:
        return 'verbe'
    elif cat1 == 2:
        return 'nom'
    elif cat1 == 3:
        return 'adjectif'
    elif cat1 == 4:
        return 'autre'
    
df['category'] = df['cat1'].apply(broad_category)

options = {}

for i, option in enumerate(df['category'].unique(), 1):
    options[i] = option
    print(f"{i}. {option}")

choice = int(input('Enter the number of the category you want to select: '))

print('user selected', choice, options[choice])
