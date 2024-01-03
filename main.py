from datetime import date, datetime


# date_now = (datetime.today()).date()
date_now = date(2023, 12, 26)
current_year = date_now.strftime("%Y")
current_week = date_now.strftime("%W")
current_day = date_now.strftime("%A")
relative_now = datetime.toordinal(date_now)
last_year, last_week, last_day = date(int(current_year), 12, 31).isocalendar()


def get_birthdays_per_week(users):
    current_week_bdays = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
        'Sunday': [],
    }
    next_week_bdays = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
        'Sunday': [],
    }

    if len(users) == 0:
        return {}
    else:
        for user in users:
            # Birthday converting block:
            get_birthday = user.get("birthday")
            user_birthday, user_birthday[0] = str(get_birthday).split('-'), current_year
            converted_date = '-'.join(_ for _ in user_birthday)
            this_year_user_bday = (datetime.strptime(converted_date, '%Y-%m-%d')).date()
            relative_user_bday = datetime.toordinal(this_year_user_bday)

            # Name converting block:
            get_full_name = user.get("name")
            name = get_full_name.split(" ")[0]

            # For past birthdays. Check the next year birthday date:
            if relative_now > relative_user_bday:
                get_birthday = user.get("birthday")
                user_birthday, user_birthday[0] = str(get_birthday).split('-'), str(int(current_year) + 1)
                converted_date = '-'.join(_ for _ in user_birthday)
                this_year_user_bday = (datetime.strptime(converted_date, '%Y-%m-%d')).date()
                relative_user_bday = datetime.toordinal(this_year_user_bday)

            # Placing names to dictionary:
            if (relative_now + 7) >= relative_user_bday >= relative_now:
                user_bday_week_number = this_year_user_bday.strftime('%W')
                if int(user_bday_week_number) == int(current_week):
                    current_week_bdays[str(this_year_user_bday.strftime('%A'))].append(name)
                else:
                    next_week_bdays[str(this_year_user_bday.strftime('%A'))].append(name)

        # Replacing weekend birthdays to next week:
        for day, birthdays in current_week_bdays.items():
            if day in ['Saturday', 'Sunday']:
                next_week_bdays['Monday'].extend(birthdays)
                current_week_bdays[day] = []


    # Dictionaries sorting:
    keys_to_delete = [key for key, value in current_week_bdays.items() if value == []]
    for key in keys_to_delete:
        del current_week_bdays[key]

    keys_to_delete = [key for key, value in next_week_bdays.items() if value == []]
    for key in keys_to_delete:
        del next_week_bdays[key]

    current_week_bdays.update(next_week_bdays)

    # Bug fixing???:
    if 'Monday' in current_week_bdays and len(current_week_bdays['Monday']) >=2:
        current_week_bdays['Monday'][0], current_week_bdays['Monday'][1] = current_week_bdays['Monday'][1], current_week_bdays['Monday'][0]


    print(current_week_bdays)
    return current_week_bdays


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 12, 29).date()},
        {"name": "JohnTest1", "birthday": datetime(2023, 12, 16).date()},
        {"name": "DoeTest1", "birthday": datetime(2023, 12, 6).date()},
        {"name": "DoeTest5", "birthday": datetime(2023, 12, 6).date()},
        {"name": "AliceTest5", "birthday": datetime(2023, 12, 29).date()},
        {"name": "JohnTest5", "birthday": datetime(2021, 12, 31).date()},
        {"name": "DoeTest5", "birthday": datetime(1976, 1, 1).date()},
        {"name": "AliceTest4", "birthday": (datetime(2021, 1, 1)).date()},
        {"name": "JohnTest3", "birthday": datetime(2023, 12, 27).date()},
        {"name": "DoeTest3", "birthday": datetime(2023, 12, 29).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")