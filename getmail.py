import os
import imaplib
import email

# Dane logowania do skrzynki pocztowej
EMAIL = 'adres@wp.pl'
PASSWORD = 'hasło!'
SERVER = 'poczta.o2.pl'

if not os.path.exists(EMAIL):
    os.mkdir(EMAIL)
os.chdir(EMAIL)

# Inicjowanie połączenia z serwerem IMAP
mail = imaplib.IMAP4_SSL(SERVER)

# Logowanie
mail.login(EMAIL, PASSWORD)

# Pobieranie listy folderów
status, folders = mail.list()

# Iteracja przez listę folderów
for folder in folders:
    # Konwersja nazwy folderu do odpowiedniego formatu
    folder = folder.decode().split(' "/" ')[-1]

    # Tworzenie katalogu dla folderu
    os.makedirs(folder, exist_ok=True)

    # Wybieranie folderu
    mail.select(folder)

    # Wyszukiwanie wszystkich wiadomości w folderze
    status, data = mail.search(None, 'ALL')
    num_messages = len(data[0].split())
    
        # Iteracja przez listę wiadomości
    for num in data[0].split():
        # Pobieranie danych wiadomości
        status, data = mail.fetch(num, '(RFC822)')

        # Konwertowanie danych do obiektu Message
        msg = email.message_from_bytes(data[0][1])

        # Generowanie nazwy pliku
        filename = '{}/E-mail_{}.eml'.format(folder, num.decode('utf-8'))

        # Zapisywanie wiadomości do pliku
        with open(filename, 'wb') as f:
            f.write(data[0][1])
            print('Zapisano wiadomość nr {} z {} do folderu {}'.format(num.decode('utf-8'),num_messages ,folder))

# Zamykanie połączenia
mail.close()
mail.logout()
