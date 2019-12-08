
def write_to_file(path, data, option='w') :
    f = open(path, option)
    f.write("%s\n" % data)
    f.close()

def read_from_file(path) :
    output = []
    f = open(path, 'r')
    lines = f.readlines()
    for r in lines :
        output.append(r)

    return output
