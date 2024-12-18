# Local Device Web API

The Web API is used by the local device frontend.

The base URL of all endpoints is: `127.0.0.0:5000/api`.

All endpoints return `Status: 200` for success and `Status: 500` for errors. 

## IoT Devices


## Energy Saving Goals

### Get All Goals

Fetches all goals.

#### Request

| Parameter | Type    | Required | Description              | Default |
| --------- | ------- | -------- | ------------------------ | ------- |
| completed | Boolean | No       | Included completed goals | false   |

```URL
GET /api/goals?completed=true
```

#### Response

```
Status: 200

[
    {
        "goalId": 1,
        "name": MyGoal,
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


```URL
POST /api/goals
Content-Type: application/json

{
    "name": NewGoal,
    "target": 250
}
```

#### Response

```
Status: 200

{
    "goalId": 2,
    "name": NewGoal,
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


```URL
PUT /api/goals/<goalId>
Content-Type: application/json

{
    "name": NewGoalName,
    "target": 300
}
```

#### Response

```
Status: 200

{
    "goalId": 2,
    "name": NewGoalName,
    "target": 300,
    "progress": 0,
    "complete": false
}
```

### Delete a Goal

Delete the goal with the goal ID of `goalId`.

#### Request

```URL
DELETE /api/goals/<goalId>
Content-Type: application/json
```

#### Response

```
Status: 200
```

## Energy Records

## Report Generation and Previous Reports

## Daily Reminders

Not intended to be implemented, included for reference.

