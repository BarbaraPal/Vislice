import bottle

import model

vislice = model.Vislice()

@bottle.get('/')
def index():
    return bottle.template('./views/index.tpl')


@bottle.get('igra/<id_igre:int>')
def pokazi_igro(id_igre):
    igra, poskus = vislice.igre[id_igre]

    return bottle.template('./views/igra.tpl',
                    igra=igra, poskus=poskus)






bottle.run(reloader=True, debug=True)

