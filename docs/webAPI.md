# Local Device Web API

The Web API is used by the local device frontend.

The base URL of all endpoints is: `127.0.0.0:5000/api`.

All endpoints return `Status Code 200` for success and `Status Code 500` for errors. 

Overview:
- IoT Devices
  - `GET /devices/` - Get all devices (including querying)
  - `GET /devices/new` - Get all unconnected devices (including querying)
  - `POST /devices/` - Create a new IoT device
  - `PUT /devices/<deviceId>` - Update a device's details or state
  - `DELETE /devices/<deviceID>` - Delete an IoT device
  - `POST /devices/unlock/<deviceID>` - Requests access if PIN code setup
- Automation
  - `GET /automation/` - Get all configured automations
  - `POST /automation/` - Create a new automation
  - `PUT /automation/<automationId>` - Update an automation
  - `DELETE /automation/<automationId>` - Delete an automation
- Energy Saving Goals
  - `GET /goals/` - Get all goals (including querying)
  - `POST /goals/` - Create a new goal
  - `PUT /goals/<goalId>` - Update a goal
  - `DELETE /goals/<goalId>` - Delete a goal
- Energy Records
  - `GET /energy/` - Get energy records (including querying)
- Daily Reports
  - `GET /reports/` - Get all reports' metadata (including querying)
  - `GET /reports/<reportId>` - Get the full report
  - `DELETE /reports/<reportId>` - Delete a report
- Daily Reminders

## IoT Devices

### Get all IoT Devices

Fetches all IoT devices connected to the smart home.

#### Request 

| Parameter | Type    | Required | Description                          | Default   |
| --------- | ------- | -------- | ------------------------------------ | --------- |
| deviceId  | Integer | No       | Search for device with id            | No search |
| name      | String  | No       | Search for device starting with name | No search |
| status    | String  | No       | "Ok" \| "Fault"                      | Both      |
| roomTag   | String  | No       | Tag name to search for               | No search |
| userTag   | String  | No       | Tag name to search for               | No search |
| customTag | String  | No       | Tag name to search for               | No search |

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
        "state": { ... },
        "status": ("Ok" | "Fault"),
        "pinEnabled": true,
        "uptimeTimeStamp: "...",
        "ipAddress": "...",
        "roomTag": "Kitchen",
        "userTags": ["Person1", "Person2"],
        "customTags": ["Tag1", "Tag2"]
    }
]
```

### Get all Unconnected IoT Devices

Fetches all unconnected Iot Devices

#### Request 

```
GET /api/devices/new
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
    "state": { ... },
    "status": ("Ok" | "Fault"),
    "uptimeTimeStamp: "...",
    "ipAddress": "...",
    "roomTag": "Kitchen",
    "userTags": ["Person1", "Person2"],
    "customTags": ["Tag1", "Tag2"]
}
```

### Update an IoT Device's details/state 

Updates the IoT Device's details/state that correspond to `deeviceID`

#### Request 

| Parameter   | Type             | Required | Description        |
| ----------- | ---------------- | -------- | ------------------ |
| name        | String           | No       | device name        |
| description | String           | No       | device description |
| roomTag     | String           | No       | room tag           |
| userTags    | Array of Strings | No       | user tags          |
| customTags  | Array of Strings | No       | custom tags        |

```
PUT /api/devices/<deviceId>
{
    "name": "SmartLight",
    "description": "",
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
    "state": { ... },
    "status": ("Ok" | "Fault"),
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
DELETE /api/devices/<deviceID>
```

#### Response

```
Status Code 200
```

### Unlock an IoT device

If an IoT deivce has a pin code setup, `pinEnabled` will be true, use this endpoint to unlock the deivce.

#### Request 

| Parameter | Type   | Required | Description         |
| --------- | ------ | -------- | ------------------- |
| pin       | String | Yes      | PIN entered by user |

```
POST /api/devices/unlock/<deviceId>
{
    "pin": "0000"
}
```

#### Response

```
Status 200 for correct pin code
Status 500 for incorrect pin code
```

## Automation

`GET /automation/` - Get all configured automations

`POST /automation/` - Create a new automation

`PUT /automation/<automationId>` - Update an automation

`DELETE /automation/<automationId>` - Delete an automation

## Energy Saving Goals 

### Get All Goals

Fetches all goals.

#### Request

| Parameter | Type    | Required | Description             | Default |
| --------- | ------- | -------- | ----------------------- | ------- |
| completed | Boolean | No       | Include completed goals | false   |

```
GET /api/goals?completed=true
```

#### Response

```
[
    {
        "goalId": 1,
        "name": "MyGoal",
        "target": 200,
        "progress": 120,
        "complete": false,
        "date": "19-03-25"
    },
    ...
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
POST /api/goals
{
    "name": "NewGoal",
    "target": 250
    "date": "19-03-25"
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
    "date": "19-03-25"
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
PUT /api/goals/<goalId>
{
    "name": "NewGoalName",
    "target": 300
    "date": "19-03-25"
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
    "date": "19-03-25"
}
```

### Delete a Goal

Delete the goal with the goal ID of `goalId`.

#### Request

```
DELETE /api/goals/<goalId>
```

#### Response

```
Status: 200
```

## Energy Records

`GET /energy` - Get all energy records (optional time range, grouping, etc)


## Daily Reports

`GET /reports` - Get all reports headers

`GET /reports/latest` - Get the most recent report

`GET /reports/<reportId>` - Get the full report

`DELETE /reports/<reportId>` - Delete a report

## Daily Reminders

Not intended to be implemented, included for reference.





<!-- 

### Endpoint

Description

#### Request 

| Parameter | Type | Required | Description | Default |
| --------- | ---- | -------- | ----------- | ------- |
|           |      |          |             |         |

```
GET /api/
```

#### Response

```
```

-->