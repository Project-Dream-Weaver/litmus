[![CodeFactor](https://www.codefactor.io/repository/github/project-dream-weaver/pyre-http/badge)](https://www.codefactor.io/repository/github/project-dream-weaver/pyre-http)
# Pyre
**NOTE: THIS IS NOT PRODUCTION READY AS OF YET**
A fast asynchronous HTTP server and framework written in Rust for Python. To live and die by speed.

## Should I use this server over the existing systems?
Probably not, sure Pyre benches considerably faster than uvicorn with your typical small, plain text response benchmarks (generally 70%+ throughput increase) as soon as you put this into a real world situation I doubt you're going to get over 10% increase, you will probably get lower average latency but again by margins of around 10% so pick and choose your poison.

### Current state of Pyre:
The main server api has been implemented other than the `H2` and `WS` protocol sections.
