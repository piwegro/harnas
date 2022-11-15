# API endpoints

All non-ASCII characters are escaped, i.e. `ą` is replaced with `\u0105`.
All of the responses are **not** pretty-printed in the production environment.

## Types

At first we declare some primitive types:

### Currency

```json
{
    "name": <string>,
    "symbol": <string>,
    "value": <float>
}
```

`name`: name of the currency \
`symbol`: three letter symbol of the currency \
`value`: value of the currency


#### Example object
```json
{
    "name": "Harna\u015b",
    "symbol": "HAR",
    "value": 1.0
}
```

### Price

```json
{
    "amount": <int>,
    "currency": <Currency>
}
```

`amount`: amount of the given currency \
`currency`: currency that the amount is in


#### Example object
```json
{
    "amount": 4,
    "currency": {
      "name": "Harna\u015b",
      "symbol": "HAR",
      "value": 1
    }
  }
```

### User

```json
{
  "accepted_currencies": [
    <Currency>,
    <Currency>
  ],
  "email": <string>,
  "name": <string>,
  "uid": <string>
}
```

`accepted_currencies`: currencies accepted by the user \
`email`: user email address\
`name`: user-readable name of the user \
`uid`: unique id of the user

#### Example object
```json
{
  "accepted_currencies": [
  {
      "name": "Harna\u015b",
      "symbol": "HAR",
      "value": 1.0
    }
  ],
  "email": "karol@kucza.xyz",
  "name": "Karol",
  "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
}
```

### Offer

```json
{
  "created_at": <string>,
  "description": <string>,
  "id": <int>,
  "images": <array[<string>]>,
  "price": <Price>,
  "seller": <User>,
  "title": <string>
}
```

`created_at`: date and time of the offer creation \
`description`: description of the offer \
`id`: unique id of the offer \
`images`: array of image urls \
`price`: price of the offer \
`seller`: user that created the offer \
`title`: title of the offer


#### Example object

```json
{
  "created_at": "Mon, 31 Oct 2022 18:32:19 GMT",
  "description": "Bardzo \u0142adna p\u00f3\u0142eczka we wspania\u0142ym stanie",
  "id": 1,
  "images": [],
  "price": {
    "amount": 4,
    "currency": {
      "name": "Harna\u015b",
      "symbol": "HAR",
      "value": 1
    }
  },
  "seller": {
    "accepted_currencies": [
      {
        "name": "Harna\u015b",
        "symbol": "HAR",
        "value": 1
      }
    ],
    "email": "karol@kucza.xyz",
    "name": "Karol",
    "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
  },
  "title": "P\u00f3\u0142eczka"
}
```

### Message
```json
{
    "content": <string>,
    "is_sent": <bool,
    "message_id": <int>,
    "receiver": <User>,
    "sender": <User>,
    "sent_at": <string>
}
```

`content`: content of the message \
`is_sent`: whether the message was sent by the current user \
`message_id`: unique id of the message \
`receiver`: user that received the message \
`sender`: user that sent the message \
`sent_at`: date and time of the message creation

#### Example object
```json
{
    "content": "Dupa 12345",
    "is_sent": true,
    "message_id": 7,
    "receiver": {
        "accepted_currencies": [
            {
                "name": "Harna\u015b",
                "symbol": "HAR",
                "value": 1.0
            }
        ],
        "email": "john.doe@example.com",
        "name": "John",
        "uid": "iELOTJC3k6VMCrrtamFq7907REz1"
    },
    "sender": {
        "accepted_currencies": [
            {
                "name": "Harna\u015b",
                "symbol": "HAR",
                "value": 1.0
            }
        ],
        "email": "karol@kucza.xyz",
        "name": "Karol",
        "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
    },
    "sent_at": "Sun, 13 Nov 2022 11:21:40 GMT"
}
```

### Error
```json
{
  "error": <string>
}
```

`error`: error message

#### Example object
```json
{
  "error": "User with given email already exists"
}
```


## Endpoints

The responses in case of 5XX errors are **not** guaranteed.

### GET `/offer/<id>`
Returns offer with given id.

If the offer is found:
**200 OK**

#### Response
```
<Offer>
```

#### Example response
```json
{
  "created_at": "Mon, 31 Oct 2022 18:32:19 GMT",
  "description": "Bardzo \u0142adna p\u00f3\u0142eczka we wspania\u0142ym stanie",
  "id": 1,
  "images": [],
  "price": {
    "amount": 4,
    "currency": {
      "name": "Harna\u015b",
      "symbol": "HAR",
      "value": 1
    }
  },
  "seller": {
    "accepted_currencies": [
      {
        "name": "Harna\u015b",
        "symbol": "HAR",
        "value": 1
      }
    ],
    "email": "karol@kucza.xyz",
    "name": "Karol",
    "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
  },
  "title": "P\u00f3\u0142eczka"
}
```

If the offer is not found:
**400 Bad Request**

#### Response
```
<Error>
```

If the internal server error occurs:
**500 Internal Server Error**
#### Response
```
<Error>
```

### GET `/offers/search/<query>/<page>`
Returns offers matching given query.

Response:
200 OK
```json
INSERT EXAMPLE RESPONSE HERE
```

If the internal server error occurs:
500 Internal Server Error

### GET `/offers/<page>`
Returns offers from given page.

Response:
200 OK
```json
INSERT EXAMPLE RESPONSE HERE
```

If the internal server error occurs:
500 Internal Server Error

### GET `/user/<id>/offers`
Returns offers from given user.

If the user id is correct:
200 OK
```json
INSERT EXAMPLE RESPONSE HERE
```

If the user id is incorrect:
400 Bad Request

If the internal server error occurs:
500 Internal Server Error

### POST `/offer`
Creates new offer.

#### Request
```json
{
    "seller_id": <string>,
    "currency": <string>,
    "price": <int>,
    "title": <string>,
    "description": <string>
}
```

`seller_id`: unique ID of the seller \
`currency`: symbol of the currency \
`price`: amount of the currency \
`title`: title of the offer \
`description`: description

#### Example request
```json
{
    "seller_id": "KyumBFaY66ZdS3oG7fPZQZycKyC2",
    "currency": "HAR",
    "price": 2,
    "title": "Dupa jasia",
    "description": "Debil"
}
```

If the offer is created: 
**200 OK**

#### Response
```
<Offer>
```

#### Example response
```json
{
    "created_at": "Sun, 13 Nov 2022 11:12:03 GMT",
    "description": "Debil",
    "id": 3,
    "images": [],
    "price": {
        "amount": 2,
        "currency": {
            "name": "Harna\u015b",
            "symbol": "HAR",
            "value": 1.0
        }
    },
    "seller": {
        "accepted_currencies": [
            {
                "name": "Harna\u015b",
                "symbol": "HAR",
                "value": 1.0
            }
        ],
        "email": "karol@kucza.xyz",
        "name": "Karol",
        "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
    },
    "title": "Dupa jasia"
}
```

If the seller id is incorrect or if the currency is not accepted:
**400 Bad Request**
#### Response
```
<Error>
```

If the internal server error occurs:
**500 Internal Server Error**
#### Response
```
<Error>
```

### POST `/images`
**WIP**

### GET `/user/<id>`
Returns user with given id.

If the user is found:
**200 OK**

#### Response
```
<User>
```

#### Example response
```json
{
  "accepted_currencies": [
    {
      "name": "Harna\u015b",
      "symbol": "HAR",
      "value": 1.0
    }
  ],
  "email": "karol@kucza.xyz",
  "name": "Karol",
  "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
}
```

If the user is not found:
**400 Bad Request**

#### Response
```
<Error>
```

If the internal server error occurs:
**500 Internal Server Error**

#### Response
```
<Error>
```

### PUT `/user/<id>`
Puts the user with given id. Should be called after the user is created.

If the user is found:
**200 OK**

#### Response
```
<User>
```

#### Example response
```json
{
  "accepted_currencies": [
    {
      "name": "Harna\u015b",
      "symbol": "HAR",
      "value": 1.0
    }
  ],
  "email": "karol@kucza.xyz",
  "name": "Karol",
  "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
}
```

If the user is not found:
**400 Bad Request**

#### Response
```
<Error>
```

If the internal server error occurs:
**500 Internal Server Error**

#### Response
```
<Error>
```

### PATCH `/user/<id>`
Updates the user with given id.

**WIP**

### GET `/user/<id>/conversations`
Returns conversations from given user.


### POST `/message`
Creates new message.

Example request:
```json
{
    "sender_id": "KyumBFaY66ZdS3oG7fPZQZycKyC2",
    "receiver_id": "iELOTJC3k6VMCrrtamFq7907REz1",
    "content": "Dupa 12345"
}
```

If sending the message is successful: 200 OK
```json
{
    "content": "Dupa 12345",
    "is_sent": true,
    "message_id": 7,
    "receiver": {
        "accepted_currencies": [
            {
                "name": "Harna\u015b",
                "symbol": "HAR",
                "value": 1.0
            }
        ],
        "email": "john.doe@example.com",
        "name": "John",
        "uid": "iELOTJC3k6VMCrrtamFq7907REz1"
    },
    "sender": {
        "accepted_currencies": [
            {
                "name": "Harna\u015b",
                "symbol": "HAR",
                "value": 1.0
            }
        ],
        "email": "karol@kucza.xyz",
        "name": "Karol",
        "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
    },
    "sent_at": "Sun, 13 Nov 2022 11:21:40 GMT"
}
```

If at least one of the users is not found:
400 Bad Request

If the internal server error occurs:
500 Internal Server Error


### GET `/currencies`
Returns all currencies.

Standard response:
**200 OK**

#### Response
```json
[
  <Currency>,
  <Currency>
]
```

#### Example response
```json
[
  {
    "name": "Harna\u015b",
    "symbol": "HAR",
    "value": 1.0
  }
]
```

If the internal server error occurs:
**500 Internal Server Error**

#### Response
```
<Error>
```

### GET `/health`
Returns health status of the server.

Response if the server is healthy:
**200 OK**

#### Response (and example response)
```json
{
  "healthy": true,
  "message": null
}
```

Response if the server is unhealthy:
**500 Internal Server Error**
#### Response
```json
{
  "healthy": false,
  "message": <str>
}
```

#### Example response
```json
{
  "healthy": false,
  "message": "Database is not available"
}
```

Or no response at all if the server is down.
