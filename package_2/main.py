
import helpers as h

if __name__ == '__main__':
    l_bigg  = h.load_bigg()
    l_rxn   = h.load_reaction()
    h.set_ec_rxn(l_bigg,l_rxn)
    for item in l_rxn:
        print(str(item))
