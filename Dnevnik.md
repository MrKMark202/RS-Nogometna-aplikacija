# Dnevnik izdarde Nogometne aplikacije kao raspodjeljenog sustava

## Početak

### Priprema paketa

- Kreiranje datoteke
- Preuzimanje potrebnih paketa u visual studio code
- Kreiranje datoteke za frontend i mikroservise


### Priprema servise
- Postavljanje "requirements.txt" pod svaki servis
- Kreiranje "main.py"
- Postavljanje "Dockerfile" za svaki servis
- pokretanje docker compose za kontejnere

### Pripremanje osnovinih servisa
- Prvo sam uspostavio MongoDb servis
- Pa sam uspostavio db servis i preko njega sve ide što se tiće podataka i ovisi o MongoDb servisu
- Sljedeći je bio frontend servis kako bismo imali izgled naše stranice, te započeli sa radom

### Auth-microservice
- Kreiranje osnovnih datoteka ("db.py", "main.py", "requirement.txt", "utils.py", "routers" folder sa "auth.py" i "user.py", "Dockerfile")
- Uspostavljanje middleware-ova u "utils.py"
- Sklapanje glavne sintakse koda u "main.py"
- Spajanje na bazu sa "db.py"
- "auth.py" služi za registraciju i prijavu
- "user.py" služi za funkcije za korisnika - create, update i delete

### League-microservice
- Kreiranje osnovnih datoteka ("db.py", "main.py", "requirement.txt", "utils.py", "routers" folder sa "league.py" "Dockerfile")
- Sklapanje glavne sintakse koda u "main.py"
- Spajanje na bazu sa "db.py"
- "league.py" služi za funkcije za lige - create, update i delete
- kreirana "liga.js" na frontendu pod folder "components" -> sadrži sve glavne funkcije za ligu za ne guram sve pod ".vue"

### Club-microservice
- Kreiranje osnovnih datoteka ("db.py", "main.py", "requirement.txt", "utils.py", "routers" folder sa "club.py" "Dockerfile")
- Sklapanje glavne sintakse koda u "main.py"
- Spajanje na bazu sa "db.py"
- "club.py" služi za funkcije za lige - create, update i delete
- kreirana "klub.js" na frontendu pod folder "components" -> sadrži sve glavne funkcije za ligu za ne guram sve pod ".vue"