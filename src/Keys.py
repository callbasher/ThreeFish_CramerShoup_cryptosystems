
# function that read the key in a file
# input :
#   fichier = str
# output :
#   data = str
def readkey(fichier):
    with open(fichier, 'r') as rfile:
        data = rfile.read()
        return data


def read_tab_keys():
    with open("../data/pass.txr", 'r') as kfile:
        data = kfile.readlines()
        return data


# Takes a bytearray as input and write it in a file
# data =
def write_tab_keys(fichier, data):
    with open(fichier, 'w') as kfile:
        for i in data:
            kfile.writelines(i)


def key_to_hex(key):
    return 0
