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
  "name": <string>,
  "uid": <string>
}
```

`accepted_currencies`: currencies accepted by the user \
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
    "content": "Example message",
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

`error`: user-readable error message

#### Example object
```json
{
  "error": "User with given email already exists"
}
```

## Authorization
For the endpoints that require authorization, the `Authorization` header needs to be provided with the value 
of `Bearer <token>`, where `<token>` is the token obtained from the Google Firebase Auth API.


## General responses
Those responses might be returned by any endpoint (are not specific to any endpoint).

### 500 Internal Server Error
Might be returned if the server is unable to process the request because of
an internal issue and not because of the request itself.

#### Response
```
<Error>
```

#### Example response
```json
{
  "error": "The database cannot be accessed"
}
```

### 401 Unauthorized
Is returned when the authentication token is missing or invalid.

#### Response
```
<Error>
```

#### Example response
```json
{
  "error": "The 'Authorization' header is missing"
}
```

### 403 Forbidden
Is returned when the user is not authorized to perform the requested action.

#### Response
```
<Error>
```

#### Example response
```json
{
  "error": "You are not authorized to perform this action"
}
```

## Endpoints

The responses in case of 5XX errors are **not** guaranteed.

### GET `/offer/<id>`
Returns offer with given id.

#### Autorization
None

#### Responses

##### 200 OK
The offer with a given id was found.

###### Response body
```
<Offer>
```

###### Example response body
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
    "name": "Karol",
    "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
  },
  "title": "P\u00f3\u0142eczka"
}
```
##### 404 Not Found
The offer with a given id was not found.

###### Response body
```
<Error>
```

### GET `/offers/search/<query>/<page>`
Returns offers matching given query.

Page with id 0 is the page with the most fitting offers and is always valid.

#### Authorization
None

#### Responses

##### 200 OK

###### Response body
```json
[
    <Offer>,
    <Offer>,
    ...
]
```

###### Additional headers
| Header          | Description           |
|-----------------|-----------------------|
| `X-Total-Pages` | Total number of pages |

##### 400 Bad Request
The page number is invalid.

###### Response body
```
<Error>
```


### GET `/offers/<page>`
Returns offers from given page. Page with id 0 is the newest page and is always valid.

#### Authorization
None

#### Responses

##### 200 OK

###### Response body
```
[
  <Offer>,
  <Offer>,
  ...
]
```

###### Additional headers
| Header          | Description           |
|-----------------|-----------------------|
| `X-Total-Pages` | Total number of pages |

##### 400 Bad Request
The page id is invalid.

###### Response body
```
<Error>
```


### GET `/user/<id>/offers`
Returns offers from given user.

#### Authorization
None

#### Responses

##### 200 OK
The user with a given id was found.

###### Response body
```
[
  <Offer>,
  <Offer>,
  ...
]
```


##### 400 Bad Request
The user id is invalid.

###### Response body
```
<Error>
```


### POST `/offer`
Creates new offer.

#### Authorization
Needs to be authorized as any user.

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

##### Example request
```json
{
    "seller_id": "KyumBFaY66ZdS3oG7fPZQZycKyC2",
    "currency": "HAR",
    "price": 2,
    "title": "Beautiful offer",
    "description": "Example description of this beautiful offer"
}
```

#### Responses

##### 201 Created

###### Response body
```
<Offer>
```

###### Example response body
```json
{
    "created_at": "Sun, 13 Nov 2022 11:12:03 GMT",
    "description": "Example description of this beautiful offer",
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
        "name": "Karol",
        "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
    },
    "title": "Beautiful offer"
}
```

#### 400 Bad Request
Probable causes
- invalid seller id
- invalid currency
- currency not accepted by the seller
- invalid price
- invalid image id

#### Response
```
<Error>
```


### POST `/images`
Uploads new image.

#### Authorization
Needs to be authorized as any user.

**WIP**

### GET `/user/<id>`
Returns user with given id.

#### Authorization
None

#### Responses

##### 200 OK
The user with a given id was found.

###### Response body
```
<User>
```

###### Example response body
```json
{
  "accepted_currencies": [
    {
      "name": "Harna\u015b",
      "symbol": "HAR",
      "value": 1.0
    }
  ],
  "name": "Karol",
  "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
}
```

##### 404 Not Found
The user with a given id does not exist.

###### Response body
```
<Error>
```

### PUT `/user/<id>`
Puts the user with given id. Should be called after the user is created.

#### Authorization
None

#### Responses

##### 201 Created
The user with a given id was created in the internal database.

###### Response body
```
<User>
```

###### Example response body
```json
{
  "accepted_currencies": [
    {
      "name": "Harna\u015b",
      "symbol": "HAR",
      "value": 1.0
    }
  ],
  "name": "Karol",
  "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
}
```

##### 400 Bad Request
The user with a given id does not exist in the Firebase Auth database.

###### Response body
```
<Error>
```

##### 409 Conflict
The user with a given id already exists in the internal database.

###### Response body
```
<Error>
```


### PATCH `/user/<id>`
Updates the user with given id.

#### Authorization
Needs to be authorized as the user with given id.

**WIP**

### GET `/user/<id>/conversations`
Returns conversations for a given user.

#### Responses

##### 200 OK

###### Response body
```json
[
  <Message>,
  <Message>
]
```

##### 400 Bad Request
The user id is invalid.

#### Response body
```
<Error>
```

### POST `/message`
Creates new message.

#### Authorization
Needs to be authorized as a sender.

#### Request body
```json
{
    "sender_id": <string>,
    "receiver_id": <string>,
    "content": <string>
}
```

`sender_id`: unique ID of the sender \
`conversation_id`: unique ID of the conversation \
`content`: content of the message

##### Example request body
```json
{
    "sender_id": "KyumBFaY66ZdS3oG7fPZQZycKyC2",
    "receiver_id": "iELOTJC3k6VMCrrtamFq7907REz1",
    "content": "Test 12345"
}
```

#### Responses

##### 201 Created
When the message was created and sent.

###### Response body
```
<Message>
```

###### Example response body
```json
{
    "content": "Example test message",
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
        "name": "Karol",
        "uid": "KyumBFaY66ZdS3oG7fPZQZycKyC2"
    },
    "sent_at": "Sun, 13 Nov 2022 11:21:40 GMT"
}
```

##### 400 Bad Request
The sender or receiver id is invalid.

###### Response body
```
<Error>
```


### GET `/currencies`
Returns all currencies.

#### Authorization
None

#### Responses

##### 200 OK

###### Response body
```json
[
  <Currency>,
  <Currency>
]
```

###### Example response body
```json
[
  {
    "name": "Harna\u015b",
    "symbol": "HAR",
    "value": 1.0
  }
]
```

### GET `/health`
Returns health status of the server.

#### Authorization
None

#### Responses

##### 200 OK
The server is healthy.


###### Response body
```json
{
  "healthy": true,
  "message": null
}
```

##### 503 Service Unavailable
The server is unhealthy.

###### Response body
```json
{
  "healthy": false,
  "message": <str>
}
```

###### Example response body
```json
{
  "healthy": false,
  "message": "Database is not available"
}
```

Or no response at all if the server is down.

## General flows

### User creation
1. User is created using the appropriate client side Google Firebase Auth method.
2. A call to the internal API is made by the client to create an entry in the database by
using the PUT method on the `/user/<id>` endpoint.

### Adding offers
1. Once the user has started uploading images, the client calls the POST method on the `/image` endpoint.
2. After all the images are successfully uploaded, the client calls the POST method on the `/offer` endpoint.
