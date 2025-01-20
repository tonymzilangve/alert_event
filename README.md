# ALERT HANDLER
    Microservice for storing alert events.

### STACK
`FastAPI  | ClickHouse | NATS | Docker` 

## Common commands
### Build the images:
```bash
$ make build
```
### Run the containers:
```bash
$ make run
```
### Run tests:
```bash
$ make test
```
### Run full code check:
```bash
$ make lint
```
### Apply linter changes:
```bash
$ make format_code
```