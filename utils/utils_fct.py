from datetime import datetime, timedelta
import gspread


def get_datetime(date):
    try:
        datetime_object = datetime.strptime(date, '%m/%d/%y %H:%M')
    except ValueError as ve:
        #print('ValueError Raised:', ve)
        datetime_object = datetime.strptime(date, '%m/%d/%y %I:%M%p')
        # print(datetime_object)
    return datetime_object


def is_valid_lead(lead_row, customer_data, postal_code_set):
    datetime_date = get_datetime(lead_row['Date'])
    if datetime_date > (datetime.now() - timedelta(days=3)) and lead_row['sent'] == '':
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


def get_insert_row_nb(sheet):
    lead_ws = sheet.get_all_records()
    row_nb = 2
    for row_nb, row_value in enumerate(lead_ws, 0):
        if row_value['Date'] is not None:
            print("Valeur : {} + ' a la ligne : {}".format(row_value, row_nb))
            insert_row += 1
    return row_nb

def convert_date(lead_data):
    lead_source = lead_data
    for lead in lead_source:
        try:
            lead['Date'] = datetime.strptime(lead['Date'], '%m/%d/%y %I:%M%p')
        except ValueError:
            lead['Date'] = datetime.strptime(lead['Date'], '%m/%d/%y %H:%M')
    return lead_source

if __name__ == "__main__":
    pass