def createMicrophoneInsertFile(locations_amount: int):
    microphone_data_status = open("RAW_DATA/Microphone_status.txt", 'r', encoding="utf-8").read().splitlines()
    microphone_data_description = open("RAW_DATA/Microphone_description.txt", 'r', encoding="utf-8").read().splitlines()
    string = "INSERT INTO s311759.Microphone (status, description, translation_channel) VALUES "
    total_mics = 0              #в массиве мы храним соотношение: id локации к количеству микрофонов на ней, чтобы потом итерацией заполнить доп.таблицы
    mics_amt_on_loc = [0]       #0 здесь нужен из-за особенностей postgres - id начинается с 1, а не с 0, поэтому первый элемент должен НЕ ИМЕТЬ в себе никаких микрофонов
    for i in range(0, locations_amount):
        amt = random.randrange(5, 30)
        total_mics += amt
        mics_amt_on_loc.append(amt)
        randomchannel = [random.randrange(1, 30), random.randrange(1, 30), random.randrange(1, 30), random.randrange(1, 30), random.randrange(1, 30)]

        for j in range(0, amt):
            substring = "('" + random.choice(microphone_data_status) + "', '" + random.choice(microphone_data_description) + "', " + str(random.choice(randomchannel)) + ")"
            if j != amt - 1 or i != locations_amount - 1:
                substring += ", "
            string += substring

    string += ";"
    stream = open("INSERTS/Insert_Microphone.txt", 'w')
    stream.write(string)
    return total_mics, mics_amt_on_loc


def createCameraInsertFile(locations_amount: int):
    camera_data_status = open("RAW_DATA/Camera_status.txt", 'r', encoding="utf-8").read().splitlines()
    camera_data_description = open("RAW_DATA/Camera_description.txt", 'r', encoding="utf-8").read().splitlines()
    string = "INSERT INTO s311759.Camera (status, description, night_vision, translation_channel) VALUES "
    total_cams = 0
    cams_amt_on_loc = [0]
    for i in range(0, locations_amount):
        amt = random.randrange(15, 200)
        total_cams += amt
        cams_amt_on_loc.append(amt)
        randomchannel = [random.randrange(1, 100), random.randrange(1, 100), random.randrange(1, 100), random.randrange(1, 100), random.randrange(1, 100), random.randrange(1, 100), random.randrange(1, 100), random.randrange(1, 100), random.randrange(1, 100)]

        for j in range(0, amt):
            nvstate = randombool(1, 10)
            substring = "('" + random.choice(camera_data_status) + "', '" + random.choice(camera_data_description) + "', '" + nvstate + "', " + str(random.choice(randomchannel)) + ")"
            if j != amt - 1 or i != locations_amount - 1:
                substring += ", "
            string += substring

    string += ";"
    stream = open("INSERTS/Insert_Camera.txt", 'w')
    stream.write(string)
    return total_cams, cams_amt_on_loc


def createMicrophones_on_LocationsInsertFile(locations_amount, mics_amt_on_loc):
    string = "INSERT INTO s311759.Microphones_on_Locations (microphone_id, location_id) VALUES "
    c = 1
    for i in range(1, locations_amount + 1):
        for j in range(0, mics_amt_on_loc[i]):
            substring = "(" + str(c) + ", " + str(i) + ")"
            c += 1
            if j != mics_amt_on_loc[i] - 1 or i != locations_amount:
                substring += ", "
            string += substring

    string += ";"
    stream = open("INSERTS/Insert_Micsonlocs.txt", 'w')
    stream.write(string)
    return


def createCameras_on_LocationsInsertFile(locations_amount, cams_amt_on_loc):
    string = "INSERT INTO s311759.Cameras_on_Locations (camera_id, location_id) VALUES "
    c = 1
    for i in range(1, locations_amount + 1):
        for j in range(0, cams_amt_on_loc[i]):
            substring = "(" + str(c) + ", " + str(i) + ")"
            c += 1
            if j != cams_amt_on_loc[i] - 1 or i != locations_amount:
                substring += ", "
            string += substring

    string += ";"
    stream = open("INSERTS/Insert_Camsonlocs.txt", 'w')
    stream.write(string)
    return