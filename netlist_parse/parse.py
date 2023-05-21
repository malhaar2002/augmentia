from kinparse import parse_netlist

def form_string(ref, func, num):
    if func != '':
        return f"{ref}_{func}"
    else:
        if num == '1':
            return f"{ref}_K"
        elif num == '2':
            return f"{ref}_A"

def parse(circuit):
    nlst = parse_netlist(circuit)

    result_json = {}

    connected_nets = [i for i in nlst.nets if 'unconnected' not in i.name]

    for connection_list in connected_nets:
        pins = connection_list.pins
        key = form_string(pins[0].ref, pins[0].function, pins[0].num)
        value = form_string(pins[1].ref, pins[1].function, pins[1].num)
        result_json[key] = value

    return result_json

if __name__ == '__main__':
    print(parse('circuits/Circuits.net'))
