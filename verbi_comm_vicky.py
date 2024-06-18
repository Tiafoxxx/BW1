# Importazione della libreria requests usata per richieste HTTP
import requests 

def main():
    # Input dell'utente per l'host e la porta
    host = input("Inserisci url dell'host: ") # Richiesta di URL da verificare
    porta = input("Inserisci porta: ")      # Richiesta di porta da verificare
    
    # Identificazione dell'URL in base alla porta
    if porta == "80":                         # Se l'utente inserisce porta 80
        url = f"http://{host}:{porta}"        # il codice crea URL HTTP
    elif porta == "443":                      # Se l'utente inserisce porta 443
        url = f"https://{host}:{porta}"       # il codice crea URL HTTPS
    else:                                     # Se la porta è diversa da 80 e 443
        print("Controlla la porta inserita!") # il codice stampa messaggio di errore
        return                                # e termina esecuzione programma

    # Stampa dell'URL che verrà verificato
    print(f"Verifico: {url}")

    try:
        # Invio della richiesta HTTP OPTIONS
        risposta = requests.options(url)
        # Controllo del codice di stato della risposta
        if risposta.status_code == 200: # se il codice è 200 la richiesta è eseguita
            # Controllo se l'intestazione 'Allow' è presente nella risposta
            if 'Allow' in risposta.headers: # se la risposta contiene header Allow
                metodi = risposta.headers['Allow'] # indica i metodi HTTP supportati
                print(f"Ecco i metodi abilitati: {metodi}") # e li stampa
            else: # Se la risposta del server non contiene header Allow
                print("Allow non è presente nella risposta\n") # stampa messaggio di errore
        else: # Se il codice di stato non è 200
            print(f"Codice di stato: {risposta.status_code}") # stampa il codice di stato
    # Gestione delle eccezioni per errori nella richiesta HTTP
    except requests.RequestException as e:         
        print(f"Errore nella richiesta: {e}")


# Verifica se il modulo è eseguito direttamente e non importato da un altro file py
if __name__ == "__main__": # Se la condizione è vera la condizione main() viene chiamata
    main()
