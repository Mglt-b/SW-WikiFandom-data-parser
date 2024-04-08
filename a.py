import requests

# L'URL de la requête de tracking
url = "https://stats.g.doubleclick.net/j/collect"

# Les données à envoyer dans le corps de la requête POST.
# Ici, vous devez remplir avec les données appropriées que vous souhaitez tracker.
data = {
    't': 'dc',
    'aip': 1,
    '_r': 3,
    'v': 1,
    '_v': 'j101',
    'tid': 'UA-32129070-1',  # ID de tracking; assurez-vous d'utiliser votre propre ID.
    'cid': '457626455.1707906018',
    'jid': '437145997',
    'gjid': '655211648',
    '_gid': '1741610772.1712563439',
    '_u': 'SCCAgEABAAAAAGAAIAB~',
    'z': '1014784259'
}

# Les en-têtes de la requête, simulant ceux d'un navigateur web.
headers = {
    'Content-Type': 'text/plain',
    'Origin': 'https://summonerswar.fandom.com',
    'Referer': 'https://summonerswar.fandom.com/',
    'User-Agent': 'Mozilla/5.0'
}

# Effectuer la requête POST
response = requests.post(url, headers=headers, data=data, verify=False)

# Vérifier le statut de la réponse
if response.status_code == 200:
    print("Requête de tracking envoyée avec succès.")
    print(response)
else:
    print("Erreur lors de l'envoi de la requête de tracking.")