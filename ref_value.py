from kinparse import parse_netlist
from icecream import ic 

def ref_value(circuit):
    resultDict = {}
    nlst = parse_netlist(circuit)
    for i in nlst.libparts:
        resultDict[i.fields[0][1]] = i.fields[1][1]
    return resultDict

if __name__ == '__main__':
    print(ref_value('circuits/servo_motor.net'))