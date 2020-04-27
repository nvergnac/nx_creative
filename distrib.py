import gspread
import argparse
import sys
import random
from pprint import pprint
from datetime import datetime, timedelta
from operator import itemgetter
import csv

from oauth2client.service_account import ServiceAccountCredentials


from utils import utils_fct


def init():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope)
    gspread_client = gspread.authorize(creds)
    return gspread_client


def get_client_data(gspread_client, client_name):
    sheet = gspread_client.open("Base donnée client Leads").sheet1
    client_database = sheet.get_all_records()
    client_data = []
    for client in client_database:
        if client_name == client['customerName']:
            client_data.append(client)
    if len(client_data) == 1:
        return client_data[0]
    elif len(client_data) > 1:
        print("Il y a {} sources de lead disponibles :\n".format(len(client_data)))
        for i, customer in enumerate(client_data, 1):
            print("{} : {}".format(i, customer['leadSource']))
        leadsource_nb = int(
            input("Entrez le numéro de la source que vous souhaitez utiliser:\n"))
        try:
            return client_data[leadsource_nb - 1]
        except IndexError as error:
            print("La valeur sélectionnée : {} semble incorrecte.\nErreur {}".format(
                leadsource_nb, error))
    return 0


def write_lead_API(gspread_client, customer_data, lead_data):
    print(customer_data)
    lead_sheet = gspread_client.open('Leads distribués').sheet1
    row_nb = utils_fct.get_insert_row_nb(lead_sheet)
    for lead in lead_data:
        print(lead)
        utils_fct.insert_lead(lead_sheet, row_nb, lead, customer_data)
        row_nb += 1
        if row_nb > 4:
            print(row_nb)
            break
        # exit(0)
        #lead_sheet.update_cell(2, 1, lead_data['Date'])


def write_lead_CSV(customer_data, lead_data, lead_nb, options):
    csv_filename = 'lead-extract_' + \
        customer_data['customerName'] + '_' + \
        str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S")) + '.csv'
    with open(csv_filename, 'w') as f:
        fieldnames = ['Date', '1) Isolation pour', '2) Quel(s) type(s) de surface à isoler ?',
                      '3) Nom', '4) Prénom', '5) Code postal', '6) Numéro de téléphone', '7) Email', 'Sent']
        thewriter = csv.DictWriter(f, fieldnames)
        thewriter.writeheader()

        assigned_lead = 0
        lead_source = lead_data
        if options.premium is True:
            premium_lead_data = sorted(
                lead_data, key=itemgetter('Date'), reverse=True)
            lead_source = premium_lead_data
        elif options.rand is True:
            random.shuffle(lead_data)

        for lead in lead_source:
            lead['Sent'] = customer_data['customerName']
            thewriter.writerow(lead)
            assigned_lead += 1
            if assigned_lead == lead_nb:
                break


def get_available_leads(gspread_client, customer_data, options):
    valid_lead = []
    available_leads = 0
    sheet = gspread_client.open_by_key(customer_data['sourceId']).sheet1
    ws = sheet.get_all_records()
    postal_code_set = utils_fct.get_postal_code_set(customer_data)
    for lead in ws:
        if utils_fct.is_valid_lead(lead, customer_data, postal_code_set) == True:
            valid_lead.append(lead)
            available_leads += 1
    print("Il y a {} leads disponibles, combien souhaitez-vous en extraire ?".format(available_leads))
    lead_nb = int(
        input("Entrez un nombre (max:{}): \n".format(available_leads)))
    #write_lead_API(gspread_client, data, valid_lead)
    if lead_nb > 0:
        write_lead_CSV(customer_data, valid_lead, lead_nb, options)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("client_name", type=str,
                        help="Nom du client pour qui on veut extraire des leads.\n")
    parser.add_argument(
        "--premium", help="Selectionne les leads les plus récents.", action="store_true")
    parser.add_argument(
        "--rand", help="Selectionne les leads aléatoirement parmi ceux disponibles.", action="store_true")
    return parser.parse_args()


# def to_be_defined():
 #   pprint(data[0]['leadsSource'])
  #  sheet_mur_placo = client.open(data[0]['leadsSource']).sheet1
   # data_mur_placo = sheet_mur_placo.get_all_records()
    #numRow = sheet_mur_placo.row_count()

    # print(len(data_mur_placo))


if __name__ == "__main__":
    options = get_args()
    gspread_client = init()
    customer_data = get_client_data(gspread_client, options.client_name)
    if customer_data == 0:
        sys.exit("Le client {} est introuvable dans la base de client.".format(
            options.client_name))
    get_available_leads(gspread_client, customer_data, options)

    pass
