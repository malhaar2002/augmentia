from kinparse import parse_netlist

# num = 1 -> cathode
# num = 2 -> anode

def parse(circuit):
    nlst = parse_netlist(circuit)

    result_json = {}

    connected_nets = [i for i in nlst.nets if 'unconnected' not in i.name]

    for connection_list in connected_nets:
        pins = connection_list.pins
        key = f"{pins[0].ref}_{pins[0].num}"
        value = f"{pins[1].ref}_{pins[1].num}"
        result_json[key] = value

    return result_json

if __name__ == '__main__':
    print(parse('circuits/Scheme6.net'))
