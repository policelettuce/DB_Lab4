import random
import datetime
from dateutil.relativedelta import relativedelta


def randombool(truecoef, overallcoef):      #if рандомное_число_от_1_до_overallcoef <= truecoef: TRUE else FALSE
    num = random.randrange(1, overallcoef)
    if (num <= truecoef):
        return "true"
    else:
        return "false"


def random_date(start, end):                #возвращает случайную дату (datetime) между start и end
    delta = (end - start).days
    rng = random.randrange(1, delta)
    return start + datetime.timedelta(days=rng)


def createLocationInsertFile():
    location_data_name = open("RAW_DATA/Location_Name.txt", 'r', encoding="utf-8").read().splitlines()
    string = "INSERT INTO s311759.Location (name, is_truman_here) VALUES "
    for i in range(0, len(location_data_name)):
        if i == 2:
            substring = "('" + location_data_name[i] + "', true)"
        else:
            substring = "('" + location_data_name[i] + "', false)"
        if i != len(location_data_name) - 1:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Location.txt", 'w')
    stream.write(string)
    return len(location_data_name)


def createDevice_typeInsertFile():
    device_type = open("RAW_DATA/Device_types.txt", 'r', encoding="utf-8").read().splitlines()
    usages = open("RAW_DATA/Device_usages.txt", 'r', encoding="utf-8").read().splitlines()
    string = "INSERT INTO s311759.Device_type (name, usage) VALUES "
    for i in range(0, len(device_type)):
        substring = "('" + str(device_type[i]) + "', '" + str(usages[i]) + "')"
        if i != len(device_type) - 1:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Device_type.txt", 'w')
    stream.write(string)
    return len(device_type)


def createDeviceInsertFile(device_type_amount, locations_amount):
    device_status = open("RAW_DATA/Device_status.txt", 'r', encoding="utf-8").read().splitlines()
    decsriptions = open("RAW_DATA/DESCRIPTIONS.txt", 'r', encoding="utf-8").read().splitlines()
    string = "INSERT INTO s311759.Device (type_id, status, description) VALUES "
    device_amount = 0           # в массиве мы храним соотношение: id локации к количеству девайсов на ней, чтобы потом итерацией заполнить доп.таблицы
    device_amt_on_loc = [0]     # 0 здесь нужен из-за особенностей postgres - id начинается с 1, а не с 0, поэтому первый элемент должен НЕ ИМЕТЬ в себе никаких девайсов
    for i in range(0, locations_amount):
        amt = random.randrange(100, 200)
        device_amount += amt
        device_amt_on_loc.append(amt)

        for j in range(0, amt):
            substring = "(" + str(random.randrange(1, device_type_amount + 1)) + ", '" + random.choice(device_status) + "', '" + random.choice(decsriptions) + "')"
            if j != amt - 1 or i != locations_amount - 1:
                substring += ", "
            string += substring

    string += ";"
    stream = open("INSERTS/Insert_Device.txt", 'w')
    stream.write(string)
    return device_amount, device_amt_on_loc


def createDevices_on_locationsInsertFile(locations_amount, device_amt_on_loc):
    string = "INSERT INTO s311759.Devices_on_Locations (device_id, location_id) VALUES "
    c = 1
    for i in range(1, locations_amount + 1):
        for j in range(0, device_amt_on_loc[i]):
            substring = "(" + str(c) + ", " + str(i) + ")"
            c += 1
            if j != device_amt_on_loc[i] - 1 or i != locations_amount:
                substring += ", "
            string += substring

    string += ";"
    stream = open("INSERTS/Insert_Devices_on_locations.txt", 'w')
    stream.write(string)
    return


def createDaylight_cycleInsertFile():
    daytime_data = open("RAW_DATA/Daylight_cycle_data.txt", 'r', encoding="utf-8").read().splitlines()
    string = "INSERT INTO s311759.Daylight_cycle (daytime) VALUES "
    for i in range (0, len(daytime_data)):
        substring = "('" + daytime_data[i] + "')"
        if i != len(daytime_data) - 1:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Daylight_cycle.txt", 'w')
    stream.write(string)
    return len(daytime_data)


def createWeatherInsertFile():
    string = "INSERT INTO s311759.Weather (temperature, precipitation, wind_speed, wind_direction) VALUES "
    directions = ["North", "South", "West", "East", "North-West", "North-East", "South-West", "South-East"]
    for i in range(0, 729):
        temperature = 0
        precipitation = 0
        wind = 0
        wind_direction = random.choice(directions)
        if i//243 == 0:
            temperature = random.randrange(-15, -1)
        elif i//243 == 1:
            temperature = random.randrange(0, 20)
        elif i//243 == 2:
            temperature = random.randrange(21, 32)

        if i//81 == 1 or i//81 == 4 or i//81 == 7:
            precipitation = 0
        elif i//81 == 2 or i//81 == 5 or i//81 == 8:
            precipitation = random.randrange(1, 20)
        elif i//81 == 3 or i//81 == 6 or i//81 == 9:
            precipitation = random.randrange(60, 100)

        if i//27 == 1 or i//27 == 4 or i//27 == 7 or i//27 == 10 or i//27 == 13 or i//27 == 16 or i//27 == 19 or i//27 == 22 or i//27 == 25:
            wind = random.randrange(0, 2)
        elif i//27 == 2 or i//27 == 5 or i//27 == 8 or i//27 == 11 or i//27 == 14 or i//27 == 17 or i//27 == 20 or i//27 == 23 or i//27 == 26:
            wind = random.randrange(3, 8)
        elif i//27 == 3 or i//27 == 6 or i//27 == 9 or i//27 == 12 or i//27 == 15 or i//27 == 18 or i//27 == 21 or i//27 == 24 or i//27 == 27:
            wind = random.randrange(9, 16)

        substring = "(" + str(temperature) + ", " + str(precipitation) + ", " + str(wind) + ", '" + wind_direction + "')"
        if i != 728:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Weather.txt", 'w')
    stream.write(string)
    return 729


def createHumanInsertFile():
    human_first_names = open("RAW_DATA/Human_first_names.txt", 'r', encoding="utf-8").read().splitlines()
    human_last_names = open("RAW_DATA/Human_last_names.txt", 'r', encoding="utf-8").read().splitlines()
    human_status = open("RAW_DATA/Human_status.txt", 'r', encoding="utf-8").read().splitlines()
    status = human_status[0]
    human_amount = random.randrange(4000, 5000)
    string = "INSERT INTO s311759.Human (full_name, status) VALUES "
    humans_working = []
    humans_fired = []
    for i in range(1, human_amount + 1):
        name = random.choice(human_first_names) + " " + random.choice(human_last_names)
        rng = random.randrange(1, 20)
        if rng <= 16:
            status = human_status[0]
            humans_working.append(i)
        elif rng == 17:
            status = human_status[1]
        elif rng == 18:
            status = human_status[2]
        elif rng > 18:
            status = human_status[3]
            humans_fired.append(i)      #для тех, кто дунул и не пришел на работу (уволенные. Контракт должен истечь ДО сегодня)
        substring = "('" + name + "', '" + status + "')"
        if i != human_amount:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Human.txt", 'w')
    stream.write(string)
    return human_amount, humans_working, humans_fired


def createVacationsInsertFile(human_amount):
    d1 = datetime.date(year=2010, month=1, day=1)
    d2 = datetime.date(year=2022, month=11, day=27)
    vacation_days = [14, 21, 28, 35, 42]
    illness_days = [7, 14]
    string = "INSERT INTO s311759.Vacations (human_id, type, vacation_start, vacation_end) VALUES "
    amount_of_vacations = random.randrange(20000, 25000)
    for i in range(0, amount_of_vacations):
        random_human_id = random.randrange(1, human_amount)
        rng = random.randrange(1, 50)
        if rng == 21:
            date = random_date(d1, d2)
            nextdate = date + datetime.timedelta(days=random.choice(illness_days))
            substring = "(" + str(random_human_id) + ", 'Illness', '" + str(date) + "', '" + str(nextdate) + "')"
        else:
            date = random_date(d1, d2)
            nextdate = date + datetime.timedelta(days=random.choice(vacation_days))
            substring = "(" + str(random_human_id) + ", 'Vacation', '" + str(date) + "', '" + str(nextdate) + "')"

        if i != amount_of_vacations - 1:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Vacation.txt", 'w')
    stream.write(string)
    return amount_of_vacations


def createJobInsertFile():
    jobs = open("RAW_DATA/Jobs.txt", 'r', encoding="utf-8").read().splitlines()
    decsriptions = open("RAW_DATA/DESCRIPTIONS.txt", 'r', encoding="utf-8").read().splitlines()
    string = "INSERT INTO s311759.Job (title, description, salary) VALUES "
    for i in range(0, len(jobs)):
        salary = random.randrange(50, 200) * 1000
        substring = "('" + jobs[i] + "', '" + random.choice(decsriptions) + "', " + str(salary) + ")"
        if i != len(jobs) - 1:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Job.txt", 'w')
    stream.write(string)
    return len(jobs)


def createHuman_employmentInsertFile(human_amount, job_title_amount, humans_fired):
    string = "INSERT INTO s311759.Human_employment (human_id, job_id, workday_start, workday_end, contract_start, contract_end) VALUES "
    workday_start = ["6:00:00", "8:00:00", "12:00:00", "16:00:00", "20:00:00", "0:00:00"]
    workday_end = ["14:00:00", "16:00:00", "20:00:00", "0:00:00", "4:00:00", "8:00:00"]
    contract_duration = [1, 2, 3, 5]
    today_date = datetime.date(year=2022, month=11, day=27)
    amount_of_contracts = 0
    actors = []
    actors_to_job = {}
    for i in range(1, human_amount + 1):                                                                                #по очереди строим цепочки контрактов для каждого человека
        human_job = random.randrange(1, job_title_amount)
        temp_date = random_date(datetime.date(year=2010, month=1, day=1), datetime.date(year=2017, month=11, day=20))   #получаем случайную дату заключения первого контракта
        while temp_date <= today_date:                                                                                  #пока контракт не продлен ЗА сегодняшнюю дату
            next_date = temp_date + relativedelta(years=random.choice(contract_duration))
            if (i in humans_fired) and (next_date > today_date):
                temp_date = next_date
            else:
                wd = random.randrange(0, 5)
                if random.randrange(1, 20) == 7: human_job = random.randrange(1, job_title_amount) #цыганские фокусы, шанс 5% что чел сменит работу на этот контракт
                substring = "(" + str(i) + ", " + str(human_job) + ", '" + workday_start[wd] + "', '" + workday_end[wd] + "', '" + str(temp_date) + "', '" + str(next_date) + "')"
                temp_date = next_date
                if i != human_amount or temp_date <= today_date:
                    substring += ", "
                string += substring
                amount_of_contracts += 1
                if human_job <= 32: actors.append(human_job)
        actors_to_job[i] = human_job

    string += ";"
    stream = open("INSERTS/Insert_Human_employment.txt", 'w')
    stream.write(string)
    return amount_of_contracts, actors, actors_to_job


def createActor_routeInsertFile():
    string = "INSERT INTO s311759.Actor_route (name, description) VALUES "
    route_name = open("RAW_DATA/Actor_route_name.txt", 'r', encoding="utf-8").read().splitlines()
    decsriptions = open("RAW_DATA/DESCRIPTIONS.txt", 'r', encoding="utf-8").read().splitlines()
    amount_of_routes = 0
    for i in range(0, len(route_name)):
        for j in range(0, len(route_name)):
            if i != j:
                name = route_name[i] + " to " + route_name[j]
                substring = "('" + str(name) + "', '" + str(random.choice(decsriptions)) + "')"
                if i != len(route_name) - 1 or j != len(route_name) - 2:
                    substring += ", "
                string += substring
                amount_of_routes += 1

    string += ";"
    stream = open("INSERTS/Insert_Actor_route.txt", 'w')
    stream.write(string)
    return amount_of_routes


def createRoutes_of_actorsInsertFile(amount_of_routes, actors):
    string = "INSERT INTO s311759.Routes_of_actors (route_id, actor_id) VALUES "
    whatever = 0
    for i in range(0, len(actors)):
        rng = random.randrange(1, 7)
        for j in range(0, rng):
            substring = "(" + str(random.randrange(1, amount_of_routes)) + ", " + str(actors[i]) + ")"
            if i != len(actors) - 1 or j != rng - 1:
                substring += ", "
            string += substring
            whatever += 1


    string += ";"
    stream = open("INSERTS/Insert_Routes_of_actors.txt", 'w')
    stream.write(string)
    return


def createScenario_stateInsertFile():
    string = "INSERT INTO s311759.Scenario_state (time_start, time_finish, is_executed, is_edited_on_air) VALUES "
    final_date = datetime.datetime(year=2022, month=11, day=27)
    curr_date = datetime.datetime(year=2010, month=1, day=1)
    exec_hours = [2, 3, 4, 5, 6]
    amount_of_scenario_states = 0
    while curr_date <= final_date:
        amount_of_scenario_states += 1
        next_date = curr_date + relativedelta(hours=random.choice(exec_hours))
        bul = randombool(23, 25)
        bul2 = randombool(13, 15)
        substring = "('" + str(curr_date) + "', '" + str(next_date) + "', " + str(bul) + ", " + str(bul2) + "), "
        string += substring
        if bul == "true":
            curr_date = next_date

    final_date = datetime.datetime(year=2023, month=11, day=27)
    amount_of_future_scenario_states = 0
    while curr_date <= final_date:
        amount_of_future_scenario_states += 1
        next_date = curr_date + relativedelta(hours=random.choice(exec_hours))
        substring = "('" + str(curr_date) + "', '" + str(next_date) + "', " + "false" + ", " + "false" + ")"
        curr_date = next_date
        if curr_date <= final_date:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Scenario_state.txt", 'w')
    stream.write(string)
    return amount_of_scenario_states, amount_of_future_scenario_states


def createScenarioInsertFile(locations_amount, daylight_cycle_amount, weather_amount):
    string = "INSERT INTO s311759.Scenario (name, description, location_id, daylight_cycle_id, weather_id, is_approved) VALUES "
    name_letters = open("RAW_DATA/Scenario_name.txt", 'r', encoding="utf-8").read().splitlines()
    decsriptions = open("RAW_DATA/DESCRIPTIONS.txt", 'r', encoding="utf-8").read().splitlines()
    approved_scenarios_amount = random.randrange(2000, 2500)
    for i in range(0, approved_scenarios_amount):
        name = str(random.choice(name_letters)) + "-" + str(random.choice(name_letters)) + "-" + str(random.choice(name_letters)) + "-" + str(random.choice(name_letters)) + "-" + str(random.choice(name_letters))
        desc = str(random.choice(decsriptions))
        location_id = random.randrange(1, locations_amount + 1)
        daylight_cycle_id = random.randrange(1, daylight_cycle_amount + 1)
        weather_id = random.randrange(1, weather_amount + 1)
        substring = "('" + name + "', '" + desc + "', " + str(location_id) + ", " + str(daylight_cycle_id) + ", " + str(weather_id) + ", true), "
        string += substring

    unapproved_scenarios_amount = random.randrange(100, 300)
    for i in range(0, unapproved_scenarios_amount):
        name = str(random.choice(name_letters)) + "-" + str(random.choice(name_letters)) + "-" + str(random.choice(name_letters)) + "-" + str(random.choice(name_letters)) + "-" + str(random.choice(name_letters))
        desc = str(random.choice(decsriptions))
        location_id = random.randrange(1, locations_amount + 1)
        daylight_cycle_id = random.randrange(1, daylight_cycle_amount + 1)
        weather_id = random.randrange(1, weather_amount + 1)
        substring = "('" + name + "', '" + desc + "', " + str(location_id) + ", " + str(daylight_cycle_id) + ", " + str(weather_id) + ", false)"
        if i != unapproved_scenarios_amount - 1:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Scenario.txt", 'w')
    stream.write(string)
    return approved_scenarios_amount, unapproved_scenarios_amount


def createScenario_scheduleInsertFile(approved_scenarios_amount, amount_of_all_scenario_states):
    string = "INSERT INTO s311759.Scenario_schedule (scenario_id, state_id) VALUES "
    for i in range(1, amount_of_all_scenario_states + 1):
        substring = "(" + str(random.randrange(1, approved_scenarios_amount)) + ", " + str(i) + ")"
        if i != amount_of_all_scenario_states:
            substring += ", "
        string += substring

    string += ";"
    stream = open("INSERTS/Insert_Scenario_schedule.txt", 'w')
    stream.write(string)
    return


def createJobs_in_scenarioInsertFile(amount_of_all_scenarios, humans_working, actors_to_job):
    string = "INSERT INTO s311759.Jobs_in_scenario (scenario_id, job_id, human_id, description) VALUES "
    decsriptions = open("RAW_DATA/DESCRIPTIONS.txt", 'r', encoding="utf-8").read().splitlines()
    for i in range(1, amount_of_all_scenarios + 1):
        rng = random.randrange(20, 120)
        for j in range(1, rng):
            random_dude_id = random.choice(humans_working)
            substring = "(" + str(i) + ", " + str(actors_to_job[random_dude_id]) + ", " + str(random_dude_id) + ", '" + str(random.choice(decsriptions)) + "')"
            if i != amount_of_all_scenarios or j != rng - 1:
                substring += ", "
            string += substring

    string += ";"
    stream = open("INSERTS/Insert_Jobs_to_scenario.txt", 'w')
    stream.write(string)
    return


def createFullInsertFile():             #скомкать все инсерты в один текстовик
    string = open("INSERTS/Insert_Location.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Device_type.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Device.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Devices_on_locations.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Daylight_cycle.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Weather.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Human.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Vacation.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Job.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Human_employment.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Actor_route.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Routes_of_actors.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Scenario_state.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Scenario.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Scenario_schedule.txt", 'r', encoding="utf-8").read()
    string += open("INSERTS/Insert_Jobs_to_scenario.txt", 'r', encoding="utf-8").read()

    print("esli tvoemu kompu ne pizda to grats")
    stream = open("INSERTS/Insert_FULL.txt", 'w')
    stream.write(string)
    stream.close()
    return


def main():
    locations_amount = createLocationInsertFile()
    device_type_amount = createDevice_typeInsertFile()
    device_amount, device_amt_on_loc = createDeviceInsertFile(device_type_amount, locations_amount)

    print("locations amount: ", locations_amount)
    print("devices amount: ", device_amount)

    createDevices_on_locationsInsertFile(locations_amount, device_amt_on_loc)

    daylight_cycle_amount = createDaylight_cycleInsertFile()
    weather_amount = createWeatherInsertFile()
    human_amount, humans_working, humans_fired = createHumanInsertFile()
    print("human amount: ", human_amount)
    vacations_amount = createVacationsInsertFile(human_amount)
    print("vacations amount: ", vacations_amount)
    job_title_amount = createJobInsertFile()
    amount_of_contracts, temp, actors_to_job = createHuman_employmentInsertFile(human_amount, job_title_amount, humans_fired)
    actors = [*set(temp)]
    print("Amount of contracts: ", amount_of_contracts)
    amount_of_routes = createActor_routeInsertFile()
    print("Amount of routes: ", amount_of_routes)
    createRoutes_of_actorsInsertFile(amount_of_routes, actors)

    amount_of_scenario_states, amount_of_future_scenario_states = createScenario_stateInsertFile()
    print("Amount of scenario states: ", amount_of_scenario_states)
    approved_scenarios_amount, unapproved_scenarios_amount = createScenarioInsertFile(locations_amount, daylight_cycle_amount, weather_amount)
    print("Total scenarios: ", approved_scenarios_amount + unapproved_scenarios_amount, " approved: ", approved_scenarios_amount, " unapproved: ", unapproved_scenarios_amount)

    createScenario_scheduleInsertFile(approved_scenarios_amount, amount_of_scenario_states + amount_of_future_scenario_states)
    createJobs_in_scenarioInsertFile(approved_scenarios_amount + unapproved_scenarios_amount, humans_working, actors_to_job)

    createFullInsertFile()


main()
