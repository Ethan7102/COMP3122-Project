* /authentication/get_token: 
```
curl -X POST -v http://localhost:5000/authentication/get_token -H 'Content-Type: application/json' -d '{"username":"comp3122", "password": "comp3122"}'
```

```
curl -X POST -v http://localhost:5000/authentication/get_token -H 'authorization: 740becc4b623786cc812c956a5afb30e' -H 'Content-Type: application/json' -d '{"username":"comp3122", "password": "comp3122"}'
```