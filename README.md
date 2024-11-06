# Requirements

- Docker


# How to build
## Docker
```bash
docker build . -t powerplantapp:latest
```
after the build successfully finishes
```bash
docker run --network="host" powerplantapp
```


# Test the application
You can send a curl request with a json payload following the syntax below from your terminal. Ensure that you are in the code repository as a work directory or write out the correct relative path after the '@'-sign yourself.
```bash
curl localhost:8888/productionplan -d @example_payloads/payload1.json --header "Content-Type: application/json"
```
Result: 
```json
[{"name":"windpark1","p":90.0},{"name":"windpark2","p":21.6},{"name":"gasfiredbig1","p":368.4},{"name":"gasfiredbig2","p":0.0},{"name":"gasfiredsomewhatsmaller","p":0.0},{"name":"tj1","p":0.0}]
```