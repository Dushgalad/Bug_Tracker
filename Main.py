import json


import sys


import os


def make_report(next_id):
    severities = {'1': 'Low', '2': 'Medium', '3': 'High', '4': 'Critical'}
    severity = ''
    bug = {}
    bug["id"] = next_id
    next_id += 1
    bug["title"] = input("Please assign title for the report: ")
    bug["description"] = input("Please assign a description: ")
    while severity not in severities:
        severity = input('Select severity:'+
                    '\n1. Low\n2. Medium\n3. High\n4. Critical'+
                    '\nYour choice: ')
        if severity not in severities:
            print("Severity number not available")
    bug['severity'] = severities[severity]
    bug['status'] = 'Open'
    return bug, next_id


def view_reports(bugs:list):
    print("===== REPORTED BUGS =====\n")
    if not bugs:
        print("No bugs reported yet.")
        return
    for bug in bugs:
        print(f"Bug#{bug['id']}")
        print(f"Title: {bug['title']}")
        print(f"Description: {bug['description']}")
        print(f"Severity: {bug['severity']}")
        print(f"Status: {bug['status']}\n")
    return


def update_status(bugs:list):
    if not bugs:
        print("No bugs available to update.")
        return False
    statuses = {
    "1": "Open",
    "2": "In Progress",
    "3": "Resolved"
    }
    while True:
        search_id = input("Enter bug ID: ")
        if not search_id.isdigit():
            print("Please enter a valid number")
            continue
        search_id = int(search_id)
        for bug in bugs:
            if search_id == bug["id"]:
                print(f"Bug #{bug['id']} found!\n"+f"Title: {bug['title']}\n"+f"Current status: {bug['status']}\n")
                print("Select new status:")
                print("1. Open\n" + "2. In Progress\n" + "3. Resolved\n")
                update_choice = ''
                while update_choice not in statuses:
                    update_choice = input("Your choice: ")
                    if update_choice not in statuses:
                        print("Invalid update, try again with the given options")
                bug['status'] = statuses[update_choice]
                print(f"Bug {bug['id']} status updated to {bug['status']}.")
                return True
        print("Bug not found. Please try again.")


def save_bugs(bugs:list,next_id):
    
    data = {}
    data['bugs'] = bugs
    data['next_id'] = next_id
    try:
        with open("bugs.tmp", "w")as file:
            json.dump(data, file, indent = 4)
        os.replace('bugs.tmp', 'bugs.json')
        return True
    except OSError as error:
        print("Saving failed because of: ", error)
        return False

    
def load_bugs():
    try:
        with open("bugs.json","r") as file:
            data = json.load(file)
            if isinstance(data, list):
                print("Old JSON format")
                bugs = data
                next_id = max((bug['id'] for bug in bugs), default=0)+1
                return bugs, next_id
            elif isinstance(data, dict):
                if not isinstance(data["bugs"],list) or type(data['next_id']) is not int or data['next_id']<1:
                    print("Invalid JSON data: bugs must be a list and next_id must be a positive integer.")
                    return None, None
                bugs = data["bugs"]
                next_id = data["next_id"]
                print("New JSON format")
                return bugs, next_id
            else:
                print("Invalid JSON structure")
                return None, None
    except FileNotFoundError:
        return [], 1
    except json.JSONDecodeError:
        print("Warning: bugs.json contains invalid JSON.")
        return None, None
    except KeyError:
        print("Required data is missing")
        return None, None

    
def display_filter_menu(filter_type=''):
    if not filter_type:
        print("""===== FILTER BUGS =====\n
1. Filter by status\n2. Filter by severity\n3. Search by bug ID\n4. Return to main menu\n""")
    if filter_type == '1':
        print("""Filter by status:\n
1. Open\n2. In progress\n3. Resolved\n""")
    if filter_type == '2':
        print("""Filter by severity:\n
1. Low\n2. Medium\n3. High\n4. Critical\n""")

        
def get_filter_choice(option_filter):
    option = ''
    statuses = {'1':'Open','2':'In Progress','3':'Resolved'}
    severities = {'1':'Low','2':'Medium','3':'High','4':'Critical'}
    if option_filter == '1':
        while option not in statuses:
            display_filter_menu(option_filter)
            option = input("Your choice: ")
            if option not in statuses:
                print("Enter valid option please")
        selected_subfilter=statuses[option]
        selected_filter = 'status'
        return selected_filter,selected_subfilter
    if option_filter == '2':
        while option not in severities:
            display_filter_menu(option_filter)
            option = input("Your choice: ")
            if option not in severities:
                print("Enter valid option please")
        selected_subfilter = severities[option]
        selected_filter = 'severity'
        return selected_filter,selected_subfilter
    if option_filter == '3':
        selected_filter = 'id'
        while True:
            selected_subfilter = input("Choose id to search: ")
            if not selected_subfilter.isdigit():
                print("Please enter a valid number")
                continue
            elif int(selected_subfilter) <= 0:
                print("Bug ID must be a positive integer")
                continue
            else:
                break
        selected_subfilter = int(selected_subfilter)
        return selected_filter,selected_subfilter

    
def filtering_reports(bugs, selected_filter, subfilter):
    filtered_bugs = []
    for bug in bugs:
        if bug[selected_filter] == subfilter:
            filtered_bugs.append(bug)
    if filtered_bugs:
        view_reports(filtered_bugs)
    else:
        print("No bugs match the selected filter.")


def filter_bugs(bugs: list):
    valid_options = ['1', '2', '3', '4']
    option_filter = ''
    while option_filter not in valid_options:
        display_filter_menu()
        option_filter=input("Your choice: ")
        if option_filter in valid_options:
            if option_filter == '4':
                return
            else:
                selected_filter, selected_subfilter = get_filter_choice(option_filter)
    filtering_reports(bugs, selected_filter, selected_subfilter)


def delete_bug(bugs):
    if not bugs:
        print("No bugs available to delete.")
        return False
    while True:
        user_input = input("Enter bug ID for deletion: ")
        if not user_input.isdigit() or int(user_input) == 0:
                print("Please enter a positive integer.")
                continue
        user_input = int(user_input)
        for bug in bugs:
            if user_input == bug["id"]:
                print(f"Bug found! bug title: {bug['title']}")
                while True:
                    del_confirmation = input("Are you sure you want to delete this bug? (y/n): ")
                    if del_confirmation == 'y':
                        bugs.remove(bug)
                        return True
                    elif del_confirmation == 'n':
                        return False
                    else:
                        continue
        print("Bug not found. Please try again.")
        continue


if __name__ == "__main__":
    running = True
    bugs,next_id = load_bugs()
    if bugs is None:
        sys.exit(1)
    while running:
        print("===== BUG TRACKER =====\n")
        print("1. Report a bug\n2. View reported bugs\n3. Update bug status\n4. Search and filter bugs\n5. Delete bug\n6. Exit")
        user_input = input("Choose an option: ")
        match user_input:
            case '1':
                bug, next_id = make_report(next_id)
                bugs.append(bug)
                
                if save_bugs(bugs, next_id):
                    print("Bug saved successfully.")
                else:
                    print("Error: Bug could not be saved.")
            case '2':
                view_reports(bugs)
            case '3':
                if update_status(bugs):
                    if save_bugs(bugs, next_id):
                        print("Bug status saved successfully.")
                    else:
                        print("Error: Bug could not be saved.")
            case '4':
                filter_bugs(bugs)
            case '5':
                if delete_bug(bugs):
                    if save_bugs(bugs, next_id):
                        print("Bug deleted successfully.")
                    else:
                        print("Error: Bug could not be saved.")
            case '6':
                running = False
            case _:
                print("Try from the given input please")