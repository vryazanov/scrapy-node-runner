***UNDER DEVELOPMENT***

# node-runner
Node runner is a scrapy command designed to manage scrapy spiders via api.

This tool aims to:
1. easily launch multiple scrapy spiders on the node
1. expose api wich can be used by external scheduler
1. support graceful shutdown processes to ensure data integrity and minimal disruption
1. synchronizing its configuration with ZooKeeper, allowing seamless integration and accessibility by external scheduler

This command is supposed to used with `scrapy-node-operator` component which is under development now.

# How to test locally

1. start docker compose
1. install deps with `poetry install`
1. go into scrapy project with `cd example`
1. start scrapy node with `scrapy node`
1. send `{"id": "uniq-id-1", "spider": "quotes"}` to `http://localhost:8000/start`

Note: This document is subject to further updates.
