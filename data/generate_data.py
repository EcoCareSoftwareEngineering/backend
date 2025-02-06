energy_usage_data = [
    0.1,  # 0,
    0.1,  # 1
    0.1,  # 2
    0.1,  # 3
    0.1,  # 4
    0.1,  # 5
    0.1,  # 6
    1,  # 7
    2,  # 8
    0.1,  # 9
    0.1,  # 10
    0.1,  # 11
    0.1,  # 12
    0.1,  # 14
    0.1,  # 13
    0.1,  # 15
    0.1,  # 16
    1,  # 17
    2,  # 18
    1,  # 19
    0.5,  # 20
    0.5,  # 21
    0.3,  # 22
    0.2,  # 23
]

energy_generation_data = [
    0,  # 0,
    0,  # 1
    0,  # 2
    0,  # 3
    0,  # 4
    0,  # 5
    0,  # 6
    0.1,  # 7
    0.1,  # 8
    0.2,  # 9
    0.2,  # 10
    0.2,  # 11
    0.2,  # 12
    0.2,  # 14
    0.2,  # 13
    0.2,  # 15
    0.2,  # 16
    0.1,  # 17
    0.1,  # 18
    0.1,  # 19
    0,  # 20
    0,  # 21
    0,  # 22
    0,  # 23
]

dates = [
    "2025-01-01",
    "2025-01-02",
    "2025-01-03",
    "2025-01-04",
    "2025-01-05",
    "2025-01-06",
    "2025-01-07",
]

iot_device_usage = [
    # Light
    [
        0,  # 0,
        0,  # 1
        0,  # 2
        0,  # 3
        0,  # 4
        0,  # 5
        0,  # 6
        0,  # 7
        20,  # 8
        10,  # 9
        0,  # 10
        0,  # 11
        0,  # 12
        0,  # 14
        0,  # 13
        0,  # 15
        0,  # 16
        0,  # 17
        0,  # 18
        0,  # 19
        0,  # 20
        0,  # 21
        40,  # 22
        20,  # 23
    ],
    # TV
    [
        0,  # 0,
        0,  # 1
        0,  # 2
        0,  # 3
        0,  # 4
        0,  # 5
        0,  # 6
        0,  # 7
        20,  # 8
        10,  # 9
        0,  # 10
        0,  # 11
        0,  # 12
        0,  # 14
        0,  # 13
        0,  # 15
        0,  # 16
        0,  # 17
        40,  # 18
        60,  # 19
        20,  # 20
        0,  # 21
        0,  # 22
        0,  # 23
    ],
    # Thermostat
    [60 for _ in range(24)],
    # Fridge
    [60 for _ in range(24)],
    # Radio
    [
        0,  # 0,
        0,  # 1
        0,  # 2
        0,  # 3
        0,  # 4
        0,  # 5
        0,  # 6
        0,  # 7
        0,  # 8
        20,  # 9
        0,  # 10
        0,  # 11
        0,  # 12
        0,  # 14
        0,  # 13
        0,  # 15
        0,  # 16
        0,  # 17
        30,  # 18
        10,  # 19
        0,  # 20
        0,  # 21
        0,  # 22
        0,  # 23
    ],
    # Hall Light
    [
        0,  # 0,
        0,  # 1
        0,  # 2
        0,  # 3
        0,  # 4
        0,  # 5
        0,  # 6
        0,  # 7
        40,  # 8
        20,  # 9
        0,  # 10
        0,  # 11
        0,  # 12
        0,  # 14
        0,  # 13
        0,  # 15
        0,  # 16
        60,  # 17
        60,  # 18
        60,  # 19
        60,  # 20
        60,  # 21
        30,  # 22
        0,  # 23
    ],
    # Energy Meter
    [60 for _ in range(24)],
]

with open("data/energy_records.csv", "w") as file:
    id = 1
    file.write("energyRecordId,date,hour,energyUse,energyGeneration\n")
    for j in range(7):
        for i in range(24):
            file.write(
                f"{id},{dates[j]},{i},{energy_usage_data[i]},{energy_generation_data[i]}\n"
            )
            id += 1


with open("data/iot_device_usage.csv", "w") as file:
    id = 1
    file.write("deviceUsageId,date,hour,usage,deviceId\n")
    for date in range(7):
        for hour in range(24):
            for device_id in range(1, 8):
                file.write(
                    f"{id},{dates[date]},{hour},{iot_device_usage[device_id-1][hour]},{device_id}\n"
                )
                id += 1
