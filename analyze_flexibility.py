"""
Script Name: analyze_flexibility.py
Description: Script used to analyze the flexibility MOF structure 
Author     : Ahmad Syarwani

"""

def calculate_volume(a, b, c):
    return a * b * c

def read_pdb_file(file_path):
    models = []
    current_model = None

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('MODEL'):
                if current_model:
                    models.append(current_model)
                current_model = {'atoms': []}
            elif line.startswith('CRYST1'):
                _, a, b, c, _, _, _ = line.split()
                current_model['a'] = float(a)
                current_model['b'] = float(b)
                current_model['c'] = float(c)
            elif line.startswith('ATOM'):
                _, _, _, _, x, y, z, _, _, _ = line.split()
                current_model['atoms'].append((float(x), float(y), float(z)))

    if current_model:
        models.append(current_model)

    return models

def main():
    pdb_file = "Movie_Framework_0_final_1_1_1_VASP_1.1.1_298.000000_10000000.000000_frameworks.pdb"
    models = read_pdb_file(pdb_file)

    with open('volume.txt', 'w') as output_file:
        for i, model in enumerate(models, start=1):
            a = model['a']
            b = model['b']
            c = model['c']
            volume = calculate_volume(a, b, c)
            output_file.write(f"{i} {volume:.3f}\n")

if __name__ == "__main__":
    main()
