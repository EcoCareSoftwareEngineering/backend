# Local Device Web API

The base URL of all endpoints is: `127.0.0.0:5000/api`.

All endpoints return `Status Code 200` for success and `Status Code 500` for errors. 

For more information on data stored in the database see [models.py](../app/models.py)

Overview:
- General
  - [`GET /unlock/`](#check-if-the-smart-home-has-a-pin-enabled) - Check if the local device has a PIN enabled
  - [`POST /unlock/`](#unlock-smart-home) - Request access if PIN code setup for smart home 
- IoT Devices
  - [`GET /devices/`](#get-all-iot-devices) - Get all devices (including querying)
  - [`GET /devices/new/`](#get-all-unconnected-iot-devices) - Get all unconnected devices (including querying)
  - [`POST /devices/`](#add-a-new-iot-device) - Create a new IoT device
  - [`PUT /devices/<deviceId>/`](#update-an-iot-devices-detailsstate) - Update a device's details or state
  - [`DELETE /devices/<deviceID>/`](#delete-an-iot-device) - Delete an IoT device
  - [`POST /devices/unlock/<deviceID>/`](#unlock-an-iot-device) - Requests access if PIN code setup for IoT device
  - [`GET /devices/usage/`](#get-device-usage) - Get device usage (including querying)
- Automations
  - [`GET /automations/`](#get-all-automations) - Get all configured automations
  - [`POST /automations/`](#create-an-automation) - Create a new automation
  - [`PUT /automations/<automationId>/`](#update-an-automation) - Update an automation
  - [`DELETE /automations/<automationId>/`](#delete-an-automation) - Delete an automation
- Energy Saving Goals
  - [`GET /goals/`](#get-all-goals) - Get all goals (including querying)
  - [`POST /goals/`](#create-a-new-goal) - Create a new goal
  - [`PUT /goals/<goalId>/`](#update-a-goal) - Update a goal
  - [`DELETE /goals/<goalId>/`](#delete-a-goal) - Delete a goal
- Energy Records
  - [`GET /energy/`](#get-energy-usage) - Get energy records (including querying)
- Accounts
  - [`POST /accounts/login`](#login) - Log into an account
  - [`POST /accounts/signup`](#sign-up-for-an-account) - Sign up for an accout
- Tags
  - [`GET /tags/`](#get-all-tags) - Retrieve all tags
  - [`POST /tags/`](#add-a-new-tag) - Create a new tag
  - [`DELETE /tags/`](#delete-a-tag) - Delete a tag

## General

### Check if the Smart Home has a PIN enabled

#### Request 

```
GET /api/unlock/
```

#### Response

```
{
    "pinEnabled": false
}
```

### Unlock Smart Home

Required to unlock the API, once unlocked the API is unlocked until server is turned off. Future version of prototype will have a timeout feature.

#### Request 

| Parameter | Type   | Required | Description               |
| --------- | ------ | -------- | ------------------------- |
| pinCode   | String | Yes      | PIN Code to unlock device |

```
POST /api/unlock/
{
    "pinCode": "0000" 
}
```

#### Response

```
{
    "unlocked": false
}
```

## IoT Devices

### Get all IoT Devices

Fetches all IoT devices connected to the smart home.

#### Request 

| Parameter   | Type    | Required | Description                          | Default   |
| ----------- | ------- | -------- | ------------------------------------ | --------- |
| deviceId    | Integer | No       | Search for device with id            | No search |
| name        | String  | No       | Search for device starting with name | No search |
| status      | String  | No       | "On" \| "Off"                        | Both      |
| faultStatus | String  | No       | "Ok" \| "Fault"                      | Both      |
| roomTag     | String  | No       | Tag name to search for               | No search |
| userTag     | String  | No       | Tag name to search for               | No search |
| customTag   | String  | No       | Tag name to search for               | No search |

```
GET /api/devices/?deviceId=0&name=SmartLight&status=Ok&roomTag=...&userTag=...&customTag=...
```

#### Response

```
[
    {
        "deviceId": 0,
        "name": "SmartLight",
        "description": "",
        "state": [
            {
                "fieldName": "hue",
                "datatype": "integer",
                "value": 2
            }
        ],
        "status": ("On" | "Off"),
        "faultStatus": ("Ok" | "Fault"),
        "pinEnabled": true,
        "unlocked": false,
        "uptimeTimeStamp: "...",
        "ipAddress": "...",
        "roomTag": "Kitchen",
        "userTags": ["Person1", "Person2", ...],
        "customTags": ["Tag1", "Tag2", ...]
    }
]
```

### Get all Unconnected IoT Devices

#### Request 

```
GET /api/devices/new/
```

#### Response

```
[
    {
        "name": "SmartLight",
        "description": "",
        "ipAddress": "...",
    }
]
```

### Add a new IoT Device 

#### Request 

| Parameter | Type   | Required | Description              |
| --------- | ------ | -------- | ------------------------ |
| ipAddress | String | Yes      | IP address of new device |

```
POST /api/devices/
{
    "ipAddress": "..."
}
```

#### Response

```
{
    "deviceId": 0,
    "name": "SmartLight",
    "description": "",
    "state": [
        {
            "fieldName": "hue",
            "datatype": "integer",
            "value": 2
        }
    ],
    "status": ("On" | "Off"),
    "faultStatus": ("Ok" | "Fault"),
    "pinEnabled": true,
    "unlocked": false,
    "uptimeTimeStamp: "...",
    "ipAddress": "...",
    "roomTag": "Kitchen",
    "userTags": ["Person1", "Person2"],
    "customTags": ["Tag1", "Tag2"]
}
```

### Update an IoT Device's Details/State 

Updates the IoT Device's details/state that correspond to `deviceID`

#### Request 

| Parameter   | Type             | Required | Description        |
| ----------- | ---------------- | -------- | ------------------ |
| deviceId    | Integer          | Yes      | device ID          |
| name        | String           | No       | device name        |
| description | String           | No       | device description |
| state       | JSON             | No       | device state       |
| roomTag     | String           | No       | room tag           |
| userTags    | Array of Strings | No       | user tags          |
| customTags  | Array of Strings | No       | custom tags        |

```
PUT /api/devices/<deviceId>/
{
    "deviceId": 0
    "name": "SmartLight",
    "description": "",
    "state": [
        {
            "fieldName": "hue",
            "datatype": "integer",
            "value": 2
        }
    ],
    "roomTag": "Kitchen",
    "userTags": ["Person1", "Person2"],
    "customTags": ["Tag1", "Tag2"]
}
```

#### Response

```
{
    "deviceId": 0,
    "name": "SmartLight",
    "description": "",
    "state": [
        {
            "fieldName": "hue",
            "datatype": "integer",
            "value": 2
        }
    ],
    "status": ("On" | "Off"),
    "faultStatus": ("Ok" | "Fault"),
    "pinEnabled": true,
    "unlocked": false,
    "uptimeTimeStamp: "...",
    "ipAddress": "...",
    "roomTag": "Kitchen",
    "userTags": ["Person1", "Person2"],
    "customTags": ["Tag1", "Tag2"]
}
```

### Delete an IoT Device

Deletes the IoT device corresponding to `deviceID`

#### Request 

```
DELETE /api/devices/<deviceID>/
```

#### Response

```
Status 200 for success
Status 500 for failure
```

### Unlock an IoT device

If an IoT deivce has a pin code setup, `pinEnabled` will be true, use this endpoint to unlock the deivce. Once unlocked the device is unlocked until server is turned off. Future version of prototype will have a timeout feature.

#### Request 

| Parameter | Type   | Required | Description         |
| --------- | ------ | -------- | ------------------- |
| pin       | String | Yes      | PIN entered by user |

```
POST /api/devices/unlock/<deviceId>/
{
    "pin": "0000"
}
```

#### Response

```
Status 200 for correct pin code
Status 500 for incorrect pin code
```

### Get Device Usage

#### Request 

| Parameter  | Type    | Required | Description                                                                                                                         |
| ---------- | ------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| deviceId   | Integer | Yes      | Fetch only usage of device with device ID                                                                                           |
| timePeriod | String  | Yes      | ("Day", "Week", "Month", "Year"), fetches the usage from the search range grouped Day: Hours, Week: Days, Month: Days, Year: Months |
| rangeStart | Date    | Yes      | Start date of search range                                                                                                          |
| rangeEnd   | Date    | Yes      | End date of search range                                                                                                            |

```
GET /api/devices/usage/?deviceId=0&timePeriod=Day
```

#### Response

Response is minutes device(s) were active according to timePeriod groupings, i.e if timePeriod was Day then there will be 24 values.

```
[
    50,
    20,
    30,
]
```



## Automations

### Get all Automations

#### Request 

| Parameter | Type    | Required | Description                                                           | Default                         |
| --------- | ------- | -------- | --------------------------------------------------------------------- | ------------------------------- |
| deviceId  | Integer | No       | Fetches only the automations associated with the device with deviceId | Fetches all devices' automation |

```
GET /api/automations/?=deviceId
```

#### Response

```
[
    {
        "automationId": 0,
        "deviceId": 0,
        "dateTime": "...",
        "newState": [
            {
                "fieldName": "hue",
                "datatype": "integer",
                "value": 2
            }
        ],

    }
]
```


### Create an automation

#### Request 

| Parameter | Type    | Required | Description                                        |
| --------- | ------- | -------- | -------------------------------------------------- |
| deviceId  | Integer | Yes      | device ID of select device                         |
| dateTime  | String  | Yes      | date and Time to activate automation               |
| newState  | JSON    | Yes      | state to update device with when automation is run |

```
POST /api/automations/
{
    "deviceId": 0,
    "dateTime": "...",
    "newState": [
        {
            "fieldName": "hue",
            "datatype": "integer",
            "value": 2
        }
    ],
}
```

#### Response

```
{
    "automationId": 0,
    "deviceId": 0,
    "dateTime": "...",
    "newState": [
        {
            "fieldName": "hue",
            "datatype": "integer",
            "value": 2
        }
    ],
}
```

### Update an Automation

#### Request 

| Parameter    | Type    | Required | Description                           |
| ------------ | ------- | -------- | ------------------------------------- |
| automationId | Integer | Yes      | automation ID of automation to update |
| dateTime     | String  | No       | updated date time                     |
| newState     | JSON    | No       | Updated new state                     |

```
PUT /api/automations/<automationId>/
{
    "automationId": 0,
    "dateTime": "...",
    "newState": [
        {
            "fieldName": "hue",
            "datatype": "integer",
            "value": 2
        }
    ],
}
```

#### Response

```
{
    "automationId": 0,
    "deviceId": 0,
    "dateTime": "...",
    "newState": [
        {
            "fieldName": "hue",
            "datatype": "integer",
            "value": 2
        }
    ],

}
```

### Delete an Automation


#### Request 

| Parameter    | Type    | Required | Description                    |
| ------------ | ------- | -------- | ------------------------------ |
| automationId | Integer | Yes      | ID of automation to be deleted |

```
DELETE /api/automations/<automationId>/
```

#### Response

```
Status 200 for success
Status 500 for failure
```

## Energy Saving Goals 

### Get All Goals

Fetches all goals.

#### Request

| Parameter | Type    | Required | Description             | Default |
| --------- | ------- | -------- | ----------------------- | ------- |
| completed | Boolean | No       | Include completed goals | false   |

```
GET /api/goals/?completed=true
```

#### Response

Progress is a percentage

```
[
    {
        "goalId": 1,
        "name": "MyGoal",
        "target": 200,
        "progress": 80,
        "complete": false,
        "date": "19-03-25"
    }
]
```

### Create a New Goal

Creates a new goal.

#### Request

| Parameter | Type    | Required | Description      |
| --------- | ------- | -------- | ---------------- |
| name      | String  | No       | Name of the goal |
| target    | Integer | Yes      | Goal Target      |
| date      | String  | No       | Target Date      |


```
POST /api/goals/
{
    "name": "NewGoal",
    "target": 250
    "date": "2025-01-30"
}
```

#### Response

```
{
    "goalId": 2,
    "name": "NewGoal",
    "target": 250,
    "progress": 0,
    "complete": false
    "date": "2025-01-30"
}
```

### Update a Goal

Updates the name and/or target of the goal with the goal ID of `goalId`.

#### Request

| Parameter | Type    | Required | Description      |
| --------- | ------- | -------- | ---------------- |
| name      | String  | No       | Name of the goal |
| target    | Integer | No       | Goal Target      |
| date      | String  | No       | Target Date      |


```
PUT /api/goals/<goalId>/
{
    "name": "NewGoalName",
    "target": 300
    "date": "2025-01-30"
}
```

#### Response

```
{
    "goalId": 2,
    "name": "NewGoalName",
    "target": 300,
    "progress": 0,
    "complete": false
    "date": "2025-01-30"
}
```

### Delete a Goal

Delete the goal with the goal ID of `goalId`.

#### Request

```
DELETE /api/goals/<goalId>/
```

#### Response

```
Status 200 for success
Status 500 for failure
```

## Energy Records

### Get Energy Usage 

#### Request 

| Parameter  | Type   | Required | Description                                                                                                                   |
| ---------- | ------ | -------- | ----------------------------------------------------------------------------------------------------------------------------- |
| timePeriod | String | Yes      | ("Day", "Week", "Month", "Year") fetches data from the search range grouped Day: Hours, Week: Days, Month: Days, Year: Months |
| startDate  | String | Yes      | Start date of search range                                                                                                    |
| endDate    | String | Yes      | End date of search range                                                                                                      |

```
GET /api/?timePeriod=Day
```

#### Response

```
{
    energyUsage: [
        20, 30, 40, ...
    ]
    energyGeneration: [
        20, 10, 5, ...
    ]
}
```

## Accounts

### Login 

#### Request 

| Parameter | Type   | Required |
| --------- | ------ | -------- |
| username  | String | Yes      |
| password  | String | Yes      |

```
POST /api/accounts/login/
{
    "username": "..."
    "password": "..."
}
```

#### Response

```
Status 200 for success
Status 500 for failure
```

### Sign up for an account

#### Request 

| Parameter | Type   | Required |
| --------- | ------ | -------- |
| username  | String | Yes      |
| password  | String | Yes      |

```
POST /api/accounts/signup/
{
    "username": "..."
    "password": "..."
}
```

#### Response

```
```

## Tags

### Get all tags

#### Request 

| Parameter | Type   | Required | Description                  |
| --------- | ------ | -------- | ---------------------------- |
| type      | String | Yes      | "User" \| "Room" \| "Custom" |

```
GET /api/tags/
```

#### Response

```
[
    {
        "tagId": 0,
        "name": "..."
    },
    ...
]
```

### Add a new tag

#### Request 

| Parameter | Type   | Required | Description                  |
| --------- | ------ | -------- | ---------------------------- |
| name      | String | Yes      | Name of tag                  |
| type      | String | Yes      | "User" \| "Room" \| "Custom" |

```
POST /api/tags/
```

#### Response

```
{
    "tagId": 0,
    "name": "..."
    "type": "User" | "Room" | "Custom"
}
```

### Delete a tag

#### Request 

| Parameter | Type    | Required | Description                |
| --------- | ------- | -------- | -------------------------- |
| tagId     | Integer | Yes      | tagId of tag to be deleted |

```
DELETE /api/tags/
```

#### Response

```
Status 200 for success
Status 500 for failure
```

<!-- 

### Endpoint

Description

#### Request 

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
|           |      |          |             |

```
GET /api/
```

#### Response

```
```

-->