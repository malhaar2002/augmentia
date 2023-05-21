from kinparse import parse_netlist
from icecream import ic 

def ref_value(circuit):
    resultDict = {}
    nlst = parse_netlist(circuit)
    for i in nlst.libparts:
        # Exclude Arduino for now because all files contain it
        if i.fields[0][1] == 'A':
            continue
        resultDict[i.fields[0][1]] = i.fields[1][1]
    return resultDict

if __name__ == '__main__':
   print(ref_value('circuits/Circuits.net') )
