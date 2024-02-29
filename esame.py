class ExamException(Exception):
    pass


class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):
        data = []
        last_date = None
        try:
            with open(self.name, 'r') as file: #with: il file viene automaticamente chiuso una volta che il blocco è stato eseguito o in caso di eccezioni
                for line in file:
                    try:
                        # Divido la riga in parti utilizzando la virgola come separatore
                        parts = line.strip().split(',')
                        # Se ci sono più di due parti, prendo solo le prime due
                        parts = parts[:2]
                        # Se non ci sono esattamente due parti (solo una), passo alla riga successiva
                        if len(parts) != 2:  
                            continue # interrompe l'esecuzione del blocco di codice corrente e passare alla prossima iterazione del ciclo
                        # Estraggo la data e il numero di passeggeri
                        date, passengers = parts
                        # Divide la data in anno e mese
                        year, month = date.split('-')
                        # Se anno o mese non sono numerici, passo alla riga successiva
                        if not year.isdigit() or not month.isdigit(): #isdigit():True solo se tutti i caratteri nella stringa sono numeri interi
                            continue
                        # Rimuovo eventuali spazi bianchi dal numero di passeggeri
                        passengers = passengers.strip()
                        # Se il numero di passeggeri non è un intero positivo, passo alla riga successiva
                        if not passengers.isdigit() or int(passengers) < 0:
                            continue
                        # Se il mese non è compreso tra 1 e 12, passo alla riga successiva
                        if int(month) < 1 or int(month) > 12:
                            continue
                        # Se l'anno non è compreso tra 1949 e 1960, passo alla riga successiva
                        if (int(year) < 1949 or int(year) > 1960):
                            continue
                        # Calcolo un timestamp univoco basato su anno e mese
                        current_date = int(year) * 12 + int(month) # timestamp = numero totale di mesi trascorsi fino a quell'anno + numero del mese

                        # Controllo se il timestamp è duplicato
                        if last_date is not None and current_date == last_date:
                            raise ExamException('Duplicate timestamp, line: {}'.format(line))
                        # Controllo se il timestamp è fuori ordine
                        if last_date is not None and current_date < last_date:
                            raise ExamException('Timestamp out of order, line: {}'.format(line))

                        # Aggiorno l'ultimo timestamp letto
                        last_date = current_date
                        # Aggiunge la data e il numero di passeggeri alla lista dei dati
                        data.append([date, int(passengers)])
                    # Ignoro eventuali errori di conversione di stringhe in numeri usando int()
                    except ValueError:
                        continue
            # Se la lista di dati è vuota, solleva un'eccezione
            if not data:
                raise ExamException('Empty data list')
        # Se il file non è trovato o non è leggibile, sollevo un'eccezione
        except FileNotFoundError:
            raise ExamException('File not found or not readable')
        return data


def find_min_max(time_series):

    min_max_dict = {}

    # Inizializzo il dizionario per ogni anno
    for entry in time_series:
        # Considero l'anno dall'entry e lo uso come chiave nel dizionario
        year = entry[0].split('-')[0]
        # Se l'anno non è già presente nel dizionario, lo aggiungo con valori di minimo e massimo iniziali
        if year not in min_max_dict:
            min_max_dict[year] = {"min": float('inf'), "max": float('-inf')} # float('inf'): Impostando un valore iniziale molto alto per facilitare il processo di ricerca

    # Trovo i valori minimi e massimi per ogni anno
    for entry in time_series:
        # Estraggo la data e il numero di passeggeri dall'entry
        date, passengers = entry
        # Considero l'anno dalla data
        year, month = date.split('-')
        # Aggiorno il valore minimo se il numero di passeggeri è inferiore al minimo attuale
        if passengers < min_max_dict[year]["min"]:
            min_max_dict[year]["min"] = passengers
        # Aggiorno il valore massimo se il numero di passeggeri è superiore al massimo attuale
        if passengers > min_max_dict[year]["max"]:
            min_max_dict[year]["max"] = passengers

    # Creo le liste dei mesi con valori minimi e massimi per ogni anno
    for year in min_max_dict:
        # Estraggo i valori minimi e massimi
        min_passengers = min_max_dict[year]["min"]
        max_passengers = min_max_dict[year]["max"]
        # Inizializzo le liste dei mesi con valori minimi e massimi
        min_months = []
        max_months = []
        # Scansiono tutte le entry della time series
        for entry in time_series:
            # Estraggo la data e il numero di passeggeri
            date, passengers = entry
            # Se il numero di passeggeri corrisponde al minimo e la data è dell'anno corrente, aggiungo il mese alla lista dei minimi
            if passengers == min_passengers and date.startswith(year): #startswith(): True se una stringa inizia con il prefisso specificato
                min_months.append(date.split('-')[1])
            # Se il numero di passeggeri corrisponde al massimo e la data è dell'anno corrente, aggiungo il mese alla lista dei massimi
            elif passengers == max_passengers and date.startswith(year):
                max_months.append(date.split('-')[1])
        # Ordino e rimuovo i duplicati dalle liste dei mesi minimi e massimi
        min_max_dict[year]["min"] = sorted(set(min_months)) #set(min_months): rimuove eventuali duplicati all'interno della lista
        min_max_dict[year]["max"] = sorted(set(max_months)) #sorted(set(max_months)): ordina la lista in ordine crescente

        # Se non c'è un valore massimo, lo imposto uguale al valore minimo
        if not max_months:
            min_max_dict[year]["max"] = min_months

    return min_max_dict

#time_series_file = CSVTimeSeriesFile(name='data.csv')
#time_series = time_series_file.get_data()

#print(time_series)
#print(find_min_max(time_series))