table=['cordee','debouchevers','difficulte','estguidede','grimper','localite','participe','partiec','proposition','siteesca','typeesca','typevoie','utilisateur','voie']

res=""
for elem in table : 
    res+=f'DROP TABLE {elem} CASCADE;\n'
print(res)


with open("table_dropper.sql", 'w', encoding='utf-8') as file:
    file.write(res)
    file.close()