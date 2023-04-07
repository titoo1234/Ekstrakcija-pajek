# Ekstrakcija-pajek
## Projekt pri predmetu Iskanje in ekstrakcija podatkov s spleta 
Implementacija spletnega pajka, ki iz podanih semenskih strani najde in shrani podatke o vseh slikah, dokumentih in straneh. Obdela zgolj strani iz domen oblike *gov.si.
### Navodila za uporabo
- Ustvari in zaženi postgresql bazo na localhost, port 5432, uporabnisko ime "user" in geslo "SecretPassword"
- Dockar ukaz: <code>docker run --name postgresql-wier -e POSTGRES_PASSWORD=SecretPassword -e POSTGRES_USER=user -v $PWD/pgdata:/var/lib/postgresql/data -v $PWD/init-scripts:/docker-entrypoint-initdb.d -p 5432:5432 -d postgres:12.2</code>
- Zaženi app.py v mapi pajek z ukazom '**app.py <stevilo_niti> T**'
- **T** se uporabi samo pri prvem zagonu, pri vseh nadaljnih zagonih se **T** izpusti

