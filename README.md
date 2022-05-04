# Products microservice

## How to run the app

### Build from Dockerfile
    
```
$ docker build -t products_ms .
$ docker run -d --name products_microservice -p 80:80 products_ms
```

open API documentation at `http://localhost/docs`

### Runt it on Heroku

open API documentation at `https://app-products-ms.herokuapp.com/docs`


