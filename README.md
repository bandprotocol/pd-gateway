# pd-gateway

Boilerplate of Premium Data Provider's Gateway.

## Design Decision Discussion

1. Flask's Request, Response is used for user-implemented function because
    - It is flexible. User can get any data from requests and can produce any shape of Response.
    - It is used by google cloud function for Python.
    - As we already specify standard on how data source script send request to the Gateway,
      which is HTTP GET request, we can let the user-implemented function receive HTTP Request
      and return as HTTP Response.
2. Type checking interface required?
    - Is user required to have strong typing on user-implemented function? We already have typing but it is not restricted.
3. Flask configuration as mapping?
    - We used configuration as mapping to allow user input any type of data to configuration. User can get data from environment variables
      , then set them in the config instance.

## Example

The example usage can be found in `example.py`

In order to run the example for testing, run following command

```sh
export FLASK_ENV=development
python3 example.py
```
