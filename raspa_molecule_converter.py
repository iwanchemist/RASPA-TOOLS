"""
Script Name: raspa_molecule_converter.py
Description: Script used to convert .xyz files to .def files for use in RASPA
Author     : Ahmad Syarwani
Usage     : >>> python3 raspa_molecule_converter.py molecule.xyz molecule.def

"""
# Copyright  : Kutay B. Sezginel, 2018
# Modified by: Ahmad Syarwani, 2023-2024

# Import libraries
from ase.io import read, write  # modified by Ahmad Syarwani
import os
import sys

def write_raspa_molecule(molecule, raspa_molecule_file, code='drg', properties=None):
    """
    Write RASPA molecule definition file (rigid molecule):
    - Molecule: ASE Atoms object
        - positions: list of atomic positions -> [[x1, y1, z1], [x2, y2, z2], ...]
        - symbols: list of atom names         -> ['C', 'O', ...]
        - bonds: list of bonds                -> [[0, 1], [0, 2], [1, 5], ...]
    - raspa_molecule_file: File name for .def file

    Optional arguments:
    - code: force field code for RASPA    -> 'drg'
    - properties: molecule properties as  -> [critical_temperature, critical_pressure, accentric_factor]
    """
    t_critical, p_critical, acentric_factor = properties # modified by Ahmad Syarwani

    mol_name = os.path.basename(raspa_molecule_file).split('.')[0]
    elements, coordinates = molecule.get_chemical_symbols(), molecule.get_positions()
    bonds = molecule.get_all_distances(mic=False)  # ASE doesn't store bonds directly

    with open(raspa_molecule_file, 'w') as rm:
        rm.write(
            "# critical constants: Temperature [T], Pressure [Pa], and Acentric factor [-]\n" +
            "%.4f\n%.1f\n%.4f\n" % (t_critical, p_critical, acentric_factor) +
            "# Number of Atoms\n%i\n" % len(elements) +
            "# Number of Groups\n1\n# %s-group\nrigid\n" % mol_name +
            "# Number of Atoms\n%i\n# Atomic Positions\n" % len(elements)
        )
        for i, (atom, coor) in enumerate(zip(elements, coordinates)):
            rm.write('%2i %2s_%3s % 5.4f % 5.4f % 5.4f\n' % (i, atom, code, coor[0], coor[1], coor[2]))

        rm.write(
            "# Chiral centers Bond  BondDipoles Bend  UrayBradley InvBend  Torsion Imp." +
            " Torsion Bond/Bond Stretch/Bend Bend/Bend Bend/Torsion IntraVDW IntraCoulomb\n" +
            "               0  %3i            0    0            0       0            0" % len(bonds) +
            "             0            0         0         0       0        0            0\n" +
            "# Bond stretch: atom n1-n2, type, parameters\n"
        )
        # Write bonds - placeholder logic as ASE doesn't directly store bonds
        for i in range(len(elements)-1): # modified by Ahmad Syarwani
            rm.write("%2i %2i RIGID_BOND\n" % (i, i+1))
        rm.write("# Number of config moves\n0\n")

if __name__ == "__main__": # modified by Ahmad Syarwani
    if len(sys.argv) < 2:
        print("Usage: python3 raspa_molecule_converter.py molecule.xyz [molecule.def]")
        sys.exit(1)

    mol_file = os.path.abspath(sys.argv[1])
    print('Reading -> %s' % mol_file)
    mol = read(mol_file)

    if len(sys.argv) > 2:
        mol_name = os.path.basename(sys.argv[2]).split('.')[0]
        raspa_molecule_file = os.path.abspath(sys.argv[2])
    else:
        mol_name = os.path.basename(mol_file).split('.')[0]
        raspa_molecule_file = os.path.join(os.path.split(mol_file)[0], '%s.def' % mol_name)

    # Prompt user for critical properties
    t_critical = float(input("Enter the critical temperature (T_critical) in Kelvin: ")) # modified by Ahmad Syarwani
    p_critical = float(input("Enter the critical pressure (P_critical) in Pascals: ")) # modified by Ahmad Syarwani
    acentric_factor = float(input("Enter the acentric factor: ")) # modified by Ahmad Syarwani

    print('Writing -> %s' % raspa_molecule_file)
    write_raspa_molecule(mol, raspa_molecule_file, properties=[t_critical, p_critical, acentric_factor])
