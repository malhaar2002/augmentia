from kinparse import parse_netlist

def parse(circuit):
    nlst = parse_netlist(circuit)

    result_json = {}

    connected_nets = [i for i in nlst.nets if 'unconnected' not in i.name]

    for connection_list in connected_nets:
        pins = connection_list.pins
        key = pins[0].ref + "-" + pins[0].num
        value = {'ref': pins[1].ref, 'num': pins[1].num, 'function': pins[1].function}
        result_json[key] = value

    return result_json

if __name__ == '__main__':
    print(parse('circuits/Circuits.net'))
