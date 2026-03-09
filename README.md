# RS-Nogometna-aplikacija
Ovo je repozitorij za Nogometnu aplikaciju. Projekt za raspodijeljene sustave i blockchain

## Raspodijeljeni sustav

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

### Match-microservice
- Kreiranje osnovnih datoteka ("db.py", "main.py", "requirement.txt", "utils.py", "models.py", "routes" folder sa "match.py", "Dockerfile")
- Sklapanje glavne sintakse koda u "main.py"
- Spajanje na bazu sa "db.py"
- "match.py" služi za upravljanje utakmicama - kreiranje (uz automatski update tablice), dohvat i brisanje
- kreirana "utakmica.js" na frontendu pod folder "components" -> sadrži logiku za rad s utakmicama

### Table-microservice
- Kreiranje osnovnih datoteka ("db.py", "main.py", "requirement.txt", "utils.py", "models.py", "routes" folder sa "table.py", "Dockerfile")
- Sklapanje glavne sintakse koda u "main.py"
- Spajanje na bazu sa "db.py"
- "table.py" služi za dohvat poretka na tablici za određenu ligu ili klub
- kreirana "tablica.js" na frontendu pod folder "components" -> sadrži funkcije za prikaz tablice


# Blockchain

### Footballer-microservice
- Kreiranje osnovnih datoteka ("db.py", "main.py", "requirement.txt", "utils.py", "models.py", "routes" folder sa "footballer.py", "Dockerfile")
- Sklapanje glavne sintakse koda u "main.py"
- Spajanje na bazu sa "db.py"
- "Models.py" sadrži pydantic modele za nogometaša
- "footballer.py" služi za funkcije za nogometaše - create i dohvat
- Pri kreiranju igrača, podaci se sinkronizirano spremaju na blockchain i u MongoDB (uključujući početni ugovor u kolekciju `concrats`)
- kreirana "igrac_transfer.js" na frontendu pod folder "components" -> sadrži funkcije za nogometaše i njihove transfere

### Transfers-microservice
- Kreiranje osnovnih datoteka ("db.py", "main.py", "requirement.txt", "utils.py", "models.py", "routes" folder sa "transfer.py", "Dockerfile")
- Sklapanje glavne sintakse koda u "main.py"
- Spajanje na bazu sa "db.py"
- "transfer.py" služi za bilježenje transfera i pregled povijesti transfera
- Pri svakom transferu, sustav automatski:
  1. Zapisuje transakciju na Blockchain
  2. Sprema detalje ugovora u MongoDB (`concrats` kolekciju)
  3. Ažurira trenutni klub igrača u bazi podataka
- koristi istu "igrac_transfer.js" komponentu na frontendu

### Hard-hat (Blockchain)
- Ovaj dio sustava služi kao blockchain sloj za osiguravanje nepromjenjivosti podataka o igračima i njihovim transferima
- Hardhat je odabran jer pruža kompletno razvojno okruženje za pisanje, testiranje i postavljanje pametnih ugovora (Smart Contracts)
- Sadrži "contracts" folder s ugovorima, "scripts" za deployment, te "hardhat.config.js" za konfiguraciju mreže
- Omogućuje lokalnu simulaciju blockchain mreže tijekom razvoja

### Primarni izvor podataka i stabilnost (MongoDB + Blockchain)
- Kako bi se osigurala stabilnost podataka nakon odjave i prijave korisnika, sustav sada koristi **MongoDB (`concrats` kolekciju) kao primarni izvor podataka** za pregled ugovora.
- **Blockchain** služi kao sekundarni izvor i rezervni sustav (fallback) za starije zapise, čime se postiže maksimalna pouzdanost.
- Pri kreiranju igrača, kao datum prvog ugovora uzima se **današnji datum**, čime se osigurava točnost vremenske linije ugovora.