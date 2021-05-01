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


def capacity_available_in_center(center_data, query_date):
    # Get sessions
    try:
        sessions = center_data["sessions"]
        for session in sessions:
            is_available = session["available_capacity"] > 0
            if is_available:
                print("Vaccine appointment available at ", center_data['name'], " on:", query_date)
    except:
        print("Error fetching sessions")


def get_apts_by_pin(pin_code=100, num_days=1):
    today = datetime.datetime.today()
    date_list = [today + datetime.timedelta(days=x) for x in range(num_days)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    for query_date in date_str:
        req_str = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin_code}&date={query_date}"
        response = requests.get(req_str)
        print("Checking for ", query_date)
        if response.ok:
            response_json = response.json()
            if (response_json["centers"]):
                # Check if appointment is actually available.
                center_id_lists = response_json["centers"]
                for center in center_id_lists:
                    capacity_available_in_center(center, query_date)
                ## TODO: Take a flag and show exact appointments here.
                ## Might not be too useful as you need to go to cowin to book anyway.
            else:
                print(f"No centers available on {query_date}")
        else:
            print("Covin server seems down.")


def parse_and_fetch():
    # Just get the pin code for now.
    print("Please enter the PIN for your locality:")
    pin_code = input()
    print("Enter the number of days in future, default 7:")
    num_days = int(input())
    get_apts_by_pin(pin_code, num_days)
    print("done")


def main():
    parse_and_fetch()

if __name__ == "__main__":
    main()
