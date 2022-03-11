
import helpers as h
import constants as c

if __name__ == '__main__':
    l_bigg  = h.load_bigg()
    l_rxn   = h.load_reaction()
    h.set_ec_rxn(l_bigg,l_rxn)

    with open(c.Res_file,'w') as f:
        for item in l_rxn:
            string = item.name + "\t" + item.ec + "\n"
            f.write(string)

