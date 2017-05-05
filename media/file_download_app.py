import requests
import json
import shutil
from Crypto.Cipher import ARC4

# url = 'http://127.0.0.1:8000/'
url = 'https://limitless-bayou-79939.herokuapp.com/'

user = ''


def check_user_exists(username, password):
    payload = {"username": username, "password": password}
    headers = {'content-type': 'application/json'}
    r = requests.post(url + 'lokahi/login_accepted/', data=json.dumps(payload), headers=headers)
    data = json.loads(r.text)
    global user
    user = username
    return data['exists']


def get_report_data():
    print()
    pk = int(input("Enter the report id you would like to view "))
    tempUrl = url + "lokahi/app_report_details/" + str(pk) + "/"
    r = requests.get(tempUrl)
    data = r.json()
    if 'bad' in data:
        print("Bad report id entered")
    else:
        print("Report Id:", data['report_id'], "\nCompany Name:", data['company_name'], "\nCompany CEO:",
              data['company_ceo'],
              "\nPhone Number:", data['company_phone'])
        print("Report files: ")
        get_report_files(data['report_id'])
        if want_to_download_all_files():
            print("You've chosen to download this report's files.")
            get_picture(data['report_id'])


def get_report_files(report_id):
    print()
    payload = {"report_id": report_id}
    headers = {'content-type': 'application/json'}
    r = requests.post(url + 'lokahi/get_pictures/', data=json.dumps(payload), headers=headers)
    data = r.json()
    for i in range(len(data)):
        print(data[i]['picfile'])


def want_to_download_all_files():
    user_input = input("Do you want to download the files associated with this report? Enter y or n\n")
    return user_input == 'y'


def get_picture(report_id):
    print("Getting files...")
    payload = {"report_id": report_id}
    headers = {'content-type': 'application/json'}
    r = requests.post(url + 'lokahi/get_pictures/', data=json.dumps(payload), headers=headers)
    data = r.json()
    for i in range(len(data)):
        download_file(data[i]['picfile'])


def list_all_reports():
    temp_url = url + "lokahi/list_all_reports/"
    payload = {"user": user}
    r = requests.post(temp_url, data=json.dumps(payload))
    data = r.json()

    for i in range(len(data)):
        print(data[i]['report_id'], data[i]['company_name'])


def download_file(passed_url):
    arc = ARC4.new("lokahi")
    temp_url = url[:-1] + str(passed_url)
    filename = temp_url[temp_url.index("pictures/") + 9:]
    print("Now downloading: ", temp_url[temp_url.index("pictures/") + 9:])
    response = requests.get(temp_url, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    if filename[-7:] == ".lokahi":
        with open(filename, 'rb') as encrypted_file, open(filename[:-7], 'wb') as decrypted_file:
            for line in encrypted_file:
                decrypted_file.write(arc.decrypt(line))
    del response


def get_file_to_encrypt():
    print()
    file_name = input("Enter file name: ")
    encrypt_file(file_name)


def encrypt_file(file_name):
    try:
        open(file_name)
    except FileNotFoundError:
        print("Invalid file name!")
        return

    arc = ARC4.new("lokahi")
    with open(file_name, 'rb') as original_file, open(file_name + ".lokahi", 'wb') as encoded_file:
        for line in original_file:
            encoded_file.write(arc.encrypt(line))
    print("File encrypted! Saved as " + file_name + ".lokahi")


def main():
    while True:
        if check_user_exists(input("Enter your username "), input("Enter your password ")):
            while (True):
                print()
                user_input = int(input(
                    "Welcome, please select an option.\n "
                    "Press 1 to display all reports.\n "
                    "Press 2 to view a specific report.\n "
                    "Press 3 to encrypt a file.\n "
                    "Press 4 to quit\n"))
                if user_input == 1:
                    list_all_reports()
                if user_input == 2:
                    get_report_data()
                if user_input == 3:
                    get_file_to_encrypt()
                if user_input == 4:
                    quit()
        else:
            print("Incorrect username or password.")


main()
