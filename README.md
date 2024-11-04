## Setup

1. Clone this repo

```bash
  git clone https://github.com/RaiseCreed/api-task.git
```

2. Go to the repo directory

```bash
  cd api-task
```

3. Activate virtual enviroment

```bash
  venv\Scripts\activate
```

4. Run the app

```bash
  uvicorn App.main:app --reload
```

**App will be served at 127.0.0.1:8000**

---------------------------

In this app I'm using NBP's API to fetch current exchange rates. Exchange rates are fetched during every single order request, so all exchange rates are always up to date!


## API Reference

#### List all orders (with converted amount)

```http
  GET /orders
```

#### Get single order (with converted amount)

```http
  GET /orders/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of order to fetch |

#### Update status of the order

```http
  PUT /orders/{id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of order to change |

#### Create new order

```http
  POST /orders/
```



