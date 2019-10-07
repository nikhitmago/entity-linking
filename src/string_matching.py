import pandas as pd
import re
import jellyfish
import sys

fodors = pd.read_csv(sys.argv[1])

zagats = pd.read_csv(sys.argv[2])

fodors[['Phone', 'Cuisine']] = fodors[['Phone', 'Cuisine']].applymap(lambda x: x.replace('"', ''))
zagats[['Phone', 'Cuisine']] = zagats[['Phone', 'Cuisine']].applymap(lambda x: x.replace('"', ''))

fodors = fodors.applymap(lambda x: x.strip())
zagats = zagats.applymap(lambda x: x.strip())

alph_num_dict = {'a': '2', 'b': '2', 'c': '2',\
                 'd': '3', 'e': '3', 'f': '3',\
                 'g': '4', 'h': '4', 'i': '4',\
                 'j': '5', 'k': '5', 'l': '5',\
                 'm': '6', 'n': '6', 'o': '6',\
                 'p': '7', 'q': '7', 'r': '7', 's': '7',\
                 'u': '8', 'w': '9', 'v': '8',\
                 'w': '9', 'x': '9', 'y': '9', 'z': '9'}

def to_num(match_obj):
    match = match_obj.group(0)
    return alph_num_dict[match]

fodors['Phone1'] = fodors['Phone'].apply(lambda x: re.findall('[0-9]{3,}', re.sub('[a-z]', to_num, x.split()[0].lower().strip())))
zagats['Phone1'] = zagats['Phone'].apply(lambda x: re.findall('[0-9]{3,}', re.sub('[a-z]', to_num, x.split()[0].lower().strip())))

fodors[['area', 'ph1', 'ph2']] = pd.DataFrame(fodors.Phone1.values.tolist(), index= fodors.index)
zagats[['area', 'ph1', 'ph2']] = pd.DataFrame(zagats.Phone1.values.tolist(), index= zagats.index)

cols_to_drop = ['Phone']
fodors.drop(columns=cols_to_drop,inplace=True)
zagats.drop(columns=cols_to_drop,inplace=True)

fodors['fodors'] = fodors.index
zagats['zagats'] = zagats.index

ph = []
addr = []
cui = []
for i in range(len(zagats)):
    for j in range(len(fodors)):
        #Phone
        if (zagats.loc[i, 'Phone1'] == fodors.loc[j, 'Phone1']):
            ph.append((i+1, j+1, 1))
        else:
            ph.append((i+1, j+1, 0))
        #Address
        val = jellyfish.jaro_distance(unicode(zagats.loc[i, 'Address']), unicode(fodors.loc[j, 'Address']))
        addr.append((i+1, j+1, val))
        #Cuisine
        val = jellyfish.jaro_winkler(unicode(zagats.loc[i, 'Cuisine']), unicode(fodors.loc[j, 'Cuisine']))
        cui.append((i+1, j+1, val))

print("\nPhone number similarities\n")
print(ph)
print("\nAddress similarities\n")
print(addr)
print("\nPhone number similarities\n")
print(cui)