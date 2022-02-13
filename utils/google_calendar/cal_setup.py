from googleapiclient.discovery import build
from google.oauth2 import service_account
from utils import config as cfg


# If modifying these scopes, delete the file token.pickle.
SCOPES = [cfg.config[0]['google']["scopes"]]
SERVICE_ACCOUNT_FILE = cfg.config[0]['google']["credentials"]
SUBJECT = cfg.config[0]['google']["subject"]


def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(SUBJECT)

    if credentials.valid == False or credentials == None:
        print("Credeciais google é invalida")
        print(credentials.valid)
    else:
        print("Credeciais google é Valida")

    service = build('calendar', 'v3', credentials=delegated_credentials)

    return service
