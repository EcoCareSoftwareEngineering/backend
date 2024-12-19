# Local Device Web API

The Web API is used by the local device frontend.

The base URL of all endpoints is: `127.0.0.0:5000/api`.

All endpoints return `Status: 200` for success and `Status: 500` for errors. 

Overview:
- IoT Devices
  - `GET /devices` - Get all devices
  - `GET /devices/new` - Get all unconnected devices
  - `POST /devices` - Create a new IoT device
  - `GET /devices/<deviceId>` - Get a specific device
  - `PUT /devices/<deviceId>` - Update a device's details or state
- Energy Saving Goals
  - `GET /goals` - Get all goals
  - `POST /goals` - Create a new goal
  - `PUT /goals/<goalId>` - Update a goal
  - `DELETE /goals/<goalId>` - Delete a goal
- Energy Records
  - `GET /energy` - Get all energy records 
- Daily Reports
  - `GET /reports` - Get all reports headers
  - `GET /reports/latest` - Get the most recent report
  - `GET /reports/<reportId>` - Get the full report

## IoT Devices

`GET /devices`- get all devices' details

`GET /devices/new` - get all unconnected devices that have been detected

`POST /devices` - create a new IoT device

`GET /devices/<deviceId>` - get a specific device's details

`PUT /devices/<deviceId>` - update a device's detail or state

## Energy Saving Goals

### Get All Goals

Fetches all goals.

#### Request

| Parameter | Type    | Required | Description              | Default |
| --------- | ------- | -------- | ------------------------ | ------- |
| completed | Boolean | No       | Included completed goals | false   |

```
GET /api/goals?completed=true
```

#### Response

```
Status: 200
Body:
[
    {
        "goalId": 1,
        "name": "MyGoal",
        "target": 200,
        "progress": 120,
        "complete": false,
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


```
POST /api/goals
Content-Type: application/json
Body:
{
    "name": "NewGoal",
    "target": 250
}
```

#### Response

```
Status: 200
Body:
{
    "goalId": 2,
    "name": "NewGoal",
    "target": 250,
    "progress": 0,
    "complete": false
}
```

### Update a Goal

Updates the name and/or target of the goal with the goal ID of `goalId`.

#### Request

| Parameter | Type    | Required | Description      |
| --------- | ------- | -------- | ---------------- |
| name      | String  | No       | Name of the goal |
| target    | Integer | No       | Goal Target      |


```
PUT /api/goals/<goalId>
Content-Type: application/json
Body:
{
    "name": "NewGoalName",
    "target": 300
}
```

#### Response

```
Status: 200
Body:
{
    "goalId": 2,
    "name": "NewGoalName",
    "target": 300,
    "progress": 0,
    "complete": false
}
```

### Delete a Goal

Delete the goal with the goal ID of `goalId`.

#### Request

```
DELETE /api/goals/<goalId>
Content-Type: application/json
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

## Daily Reminders

Not intended to be implemented, included for reference.

