import os# utiliser pour le chemin d'accès

def image_dir(data_name):
    main=os.path.dirname(__file__)
    return  os.path.join(main, data_name)
