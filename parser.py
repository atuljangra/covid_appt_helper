import requests
import json
import datetime

num_states = 28 + 8
def get_district_data():
    for state_id in range(1,num_states):
        print("State code: ", state_id)
        req_str = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}"
        response = requests.get(req_str)
        try:
            json_data = json.loads(response.text)
            for i in json_data["districts"]:
                print(i["district_id"], ":", i["district_name"])
            print('\n')
        except Exception as ex:
            print(f"Error{ex}: state_id:{state_id}")
            pass

def get_apts_by_pin(pin_code, num_days=7):
    today = datetime.datetime.today()
    date_list = [today + datetime.timedelta(days=x) for x in range(num_days)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    for query_date in date_str:
        req_str = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin_code}&date={query_date}"
        print(req_str)
        response = requests.get(req_str)
        if response.ok:
            response_json = response.json()
            if (response_json["centers"]):
                print(f"You can book vaccine slots on {query_date}")
                ## TODO: Take a flag and show exact appointments here.
                ## Might not be too useful as you need to go to cowin to book anyway.
            else:
                print(f"No appointment available on {query_date}")
        else:
            print("Covin server seems down.")


def parse_and_fetch():
    # Just get the pin code for now.
    print("Please enter the PIN for your locality:")
    pin_code = input()
    print("Enter the number of days in future, default 7:")
    num_days = int(input())
    # print(pin_code, num_days)
    get_apts_by_pin(pin_code, num_days)
    print("done")


def main():
    parse_and_fetch()

if __name__ == "__main__":
    main()
