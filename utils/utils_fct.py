from datetime import datetime, timedelta
import gspread


def ask_user():
    check = str(input(
        "Voulez-vous inscrire les leads automatiquement dans la Google Sheet ? (y/n):")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print("Please enter valid inputs : 'y' or 'n'")
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs : 'y' or 'n'")
        print(error)
        return ask_user()


def get_datetime(date):
    try:
        datetime_object = datetime.strptime(date, '%m/%d/%y %H:%M')
    except ValueError:
        try:
            datetime_object = datetime.strptime(date, '%m/%d/%y %I:%M%p')
        except ValueError:
            try:
                datetime_object = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
            except ValueError as e:
                try:
                    datetime_object = datetime.strptime(date, '%m/%d/%Y %H:%M')
                except ValueError as e:
                    print("Probleme de format de date sur le fichier source des leads : {}\nVeuillez contacter Nicolas pour corriger le probleme ou essayez de changer manuellement le format de date dans la Google Sheet (Format > Nombres > Autres formats > Autre formats de dates et d'heures".format(e))
    return datetime_object


def is_valid_lead(lead_row, customer_data, postal_code_set):
    datetime_date = get_datetime(lead_row['Date'])
    if datetime_date > (datetime.now() - timedelta(days=30)) and lead_row['sent'] == '':
        if postal_code_set != 0:
            postal_code = get_postal_code(lead_row['5) Code postal'])
            if postal_code in postal_code_set:
                return True
            else:
                return False
        return True
    return False


def get_postal_code(postal_code):
    if isinstance(postal_code, int) is True:
        str_postal_code = str(postal_code)
        if len(str_postal_code) == 4:
            return int(str_postal_code[0:1])
        elif len(str_postal_code) == 5:
            return int(str_postal_code[0:2])
    return 0


def get_postal_code_set(customer_data):
    if customer_data['region'] != '':
        if type(customer_data['region']) == int:
            postal_code_set = set([customer_data['region']])
        else:
            postal_code_list = customer_data['region'].split(',')
            postal_code_list = [int(i) for i in postal_code_list]
            postal_code_set = set(postal_code_list)
        return postal_code_set
    else:
        return 0


def insert_lead(sheet, row, lead, customer_data):
    sheet.update_cell(row, 1, lead['Date'])
    sheet.update_cell(row, 2, lead['1) Isolation pour'])
    sheet.update_cell(row, 3, lead['2) Quel(s) type(s) de surface à isoler ?'])
    sheet.update_cell(row, 4, lead['3) Nom'])
    sheet.update_cell(row, 5, lead['4) Prénom'])
    sheet.update_cell(row, 6, lead['5) Code postal'])
    sheet.update_cell(row, 7, lead['6) Numéro de téléphone'])
    sheet.update_cell(row, 8, lead['7) Email'])
    sheet.update_cell(row, 9, customer_data['customerName'])


def insert_lead_in_sheet(sheet, leads):
    lead_ws = sheet.get_all_records()
    # On recupère la ligne a laquelle on souhaite insérer les leads attribués
    row_ins = len(lead_ws) + 2
    # On définit la range dans laquelle vont s'inscrire les nouveaux leads attribués
    cell_range = 'A' + str(row_ins) + ':I' + str(len(leads) + row_ins - 1)
    cells = sheet.range(cell_range)
    # On "flatten" notre liste de leads à attribué que l'on récupère depuis le csv
    flattened_data = [lead_info for lead in leads for lead_info in lead]
    # Pour chaque valeur des cellules de notre range cible, on met à jour la nouvelle valeur de chaque cellule
    for x in range(len(flattened_data)):
        cells[x].value = flattened_data[x]
    # On fait l'appel à l'API pour ecrire dans la sheet
    sheet.update_cells(cells)


def convert_date(lead_data):
    lead_source = lead_data
    for lead in lead_source:
        try:
            lead['Date'] = datetime.strptime(lead['Date'], '%m/%d/%y %I:%M%p')
        except ValueError:
            try:
                lead['Date'] = datetime.strptime(lead['Date'], '%m/%d/%y %H:%M')
            except ValueError:
                try:
                    lead['Date'] = datetime.strptime(lead['Date'], '%m/%d/%Y %H:%M:%S')
                except ValueError:
                    try:
                        lead['Date'] = datetime.strptime(lead['Date'], '%m/%d/%Y %H:%M')
                    except ValueError:
                        print("Probleme de date")

    return lead_source


if __name__ == "__main__":
    pass
