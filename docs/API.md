# Local Device Web API

The base URL of all endpoints is: `127.0.0.0:5000/api`.

All endpoints return `Status Code 200` for success and `Status Code 500` for errors. 

For more information on data stored in the database see [models.py](../app/models.py).

## Authentication

To use the API all requests must be accompanied with an Authentication token in request headers. The token is acquired by sending a request to `.../accounts/login/` with valid login credentials. The API will respond with a token to be used in future requests. `.../accounts/.../` are only endpoints that do not require a token for obvious reasons. To use the other endpoints send "token": "..." as a header in all requests.

The touchscreen frontend should use the following login credentials and make an automatic call upon startup:
- Username: "touchscreen"
- Password: "touchscreenPassword"

Remote account:
- Username: "remote"
- Password "remote123"

Testing account:
- Username: "testing"
- Password: "testing123"

## General Information

### Dates

All dates used by the API are in the format: "yyyy-mm-dd", where "yyyy" is the 4 digit year, "mm" is the 2 digit month and "dd" is the 2 digit day.

If a time is required it is in the format: "hh:mm", where "hh" is the 2 digit hour in a 24 clock and "mm" is the 2 digit minutes.

If a dateTime is required it is in the format: "yyyy-mm-dd hh:mm", see above for information.

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
  - [`POST /accounts/signup`](#sign-up-for-an-account) - Sign up for an account
- Tags
  - [`GET /tags/`](#get-all-tags) - Retrieve all tags
  - [`POST /tags/`](#add-a-new-tag) - Create a new tag
  - [`DELETE /tags/`](#delete-a-tag) - Delete a tag

## General

Still being planned, API may change. 

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
| roomTag     | Integer | No       | Tag name to search for               | No search |
| userTag     | Integer | No       | Tag name to search for               | No search |
| customTag   | Integer | No       | Tag name to search for               | No search |

```
GET /api/devices/?deviceId=0&name=SmartLight&status=Ok&roomTag=1&userTag=2&customTag=...
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
        "userTags": [
            {
                "tagId": 0,
                "name": "...",
                "type": "..."
            },
            ...
        ],
        "customTags": [
            {
                "tagId": 0,
                "name": "...",
                "type": "..."
            },
            ...
        ]
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
    "userTags": [
        {
            "tagId": 0,
            "name": "...",
            "type": "..."
        },
        ...
    ],
    "customTags": [
        {
            "tagId": 0,
            "name": "...",
            "type": "..."
        },
        ...
    ]
}
```

### Update an IoT Device's Details/State 

Updates the IoT Device's details/state that correspond to `deviceID`, only send the new details, however all tagIds must be send as the absence of a tagId is understood as removing the tag from the IoT Device.

#### Request 

| Parameter   | Type             | Required | Description        |
| ----------- | ---------------- | -------- | ------------------ |
| deviceId    | Integer          | Yes      | device ID          |
| name        | String           | No       | device name        |
| description | String           | No       | device description |
| state       | JSON             | No       | device state       |
| roomTag     | Integer          | No       | room tag           |
| userTags    | Array of Strings | No       | user tags          |
| customTags  | Array of Strings | No       | custom tags        |

```
PUT /api/devices/<deviceId>/
{
    "name": "SmartLight",
    "description": "",
    "state": [
        {
            "fieldName": "hue",
            "datatype": "integer",
            "value": 2
        }
    ],
    "roomTag": 5,
    "userTags": [0, 1, ...],
    "customTags": [2, 3, ...]
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
    "roomTag": 5,
    "userTags": [
        {
            "tagId": 0,
            "name": "...",
            "type": "..."
        },
        ...
    ],
    "customTags": [
        {
            "tagId": 0,
            "name": "...",
            "type": "..."
        },
        ...
    ]
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

If an IoT device has a pin code setup, `pinEnabled` will be true, use this endpoint to unlock the device. Once unlocked the device is unlocked until server is turned off. Future version of prototype will have a timeout feature.

#### Request 

| Parameter | Type    | Required | Description                 |
| --------- | ------- | -------- | --------------------------- |
| deviceId  | Integer | Yes      | Id of device to be unlocked |
| pin       | String  | Yes      | PIN entered by user         |

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

| Parameter  | Type    | Required | Description                               |
| ---------- | ------- | -------- | ----------------------------------------- |
| deviceId   | Integer | No       | Fetch only usage of device with device ID |
| rangeStart | Date    | Yes      | Start date of search range                |
| rangeEnd   | Date    | Yes      | End date of search range                  |

```
GET /api/devices/usage/?rangeStart=...&rangeEnd=...
```

#### Response

Each element is the number of minutes the device was active in the period of an hour. Each day has 24 entries corresponding to the 24 hour periods in a day. The array starts from the first day in the range, then second, etc.

```
[
    {
        "deviceId": 0,
        "usage": [
            {"datetime": ..., "usage": 40},
            {"datetime": ..., "usage": 20},
            {"datetime": ..., "usage": 60},
            {"datetime": ..., "usage": 20},
            ...
        ]
    },
    ...
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

Only send the new details.

#### Request 

| Parameter    | Type    | Required | Description                           |
| ------------ | ------- | -------- | ------------------------------------- |
| automationId | Integer | Yes      | automation ID of automation to update |
| dateTime     | String  | No       | updated date time                     |
| newState     | JSON    | No       | Updated new state                     |

```
PUT /api/automations/<automationId>/
{
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

Progress is a unit compared to the target, not a percentage

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

Updates the name and/or target of the goal with the goal ID of `goalId`, only send the new details.

#### Request

| Parameter | Type    | Required | Description              |
| --------- | ------- | -------- | ------------------------ |
| goalId    | Integer | Yes      | Id of goal to be updated |
| name      | String  | No       | Name of the goal         |
| target    | Integer | No       | Goal Target              |
| date      | String  | No       | Target Date              |


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

| Parameter | Type    | Required | Description              |
| --------- | ------- | -------- | ------------------------ |
| goalId    | Integer | Yes      | Id of goal to be deleted |

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

| Parameter | Type   | Required | Description                |
| --------- | ------ | -------- | -------------------------- |
| startDate | String | Yes      | Start date of search range |
| endDate   | String | Yes      | End date of search range   |

```
GET /api/?startDate=...&endDate=...
```

#### Response

Each element is the amount of energy used/generated in the period of an hour. Each day has 24 entries corresponding to the 24 hour periods in a day. The array starts from the first day in the range, then second, etc.

```
[
    {"datetime": ..., "energyUse": 40, "energyGeneration": 20},
    {"datetime": ..., "energyUse": 40, "energyGeneration": 20},
    {"datetime": ..., "energyUse": 40, "energyGeneration": 20},
    {"datetime": ..., "energyUse": 40, "energyGeneration": 20},
    {"datetime": ..., "energyUse": 40, "energyGeneration": 20},
]
```

## Accounts

### Login 

Password must be hashed string. Response is a authentication token that must be send as a header to all future requests ("token": "...").

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
{
    "token": "..."
}
```

### Sign up for an account

Password must be hashed string.

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
Status 200 for success
Status 500 for failure
```

## Tags

Tags are of type: "User", "Room" or "Custom"

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

### Get one tags

#### Request 

| Parameter | Type    | Required | Description               |
| --------- | ------- | -------- | ------------------------- |
| tagId     | Integer | Yes      | Id of tag to be retrieved |

```
GET /api/tags/<tagId>/
```

#### Response

```
{
    "tagId": 0,
    "name": "..."
    "type": "..."
}
```

### Add a new tag

#### Request 

| Parameter | Type   | Required | Description                  |
| --------- | ------ | -------- | ---------------------------- |
| name      | String | Yes      | Name of tag                  |
| type      | String | Yes      | "User" \| "Room" \| "Custom" |

```
POST /api/tags/
{
    "name": "...",
    "type": "..."
}
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

| Parameter | Type    | Required | Description             |
| --------- | ------- | -------- | ----------------------- |
| tagId     | Integer | Yes      | Id of tag to be deleted |

```
DELETE /api/tags/<tagId>/
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