***UNDER DEVELOPMENT***

# node-runner
Node runner is an application designed to manage Scrapy projects and spiders on a single node.

This tool aims to:
1. easily launch multiple Scrapy projects installed on the node
1. expose key metrics for seamless auto-scaling
1. support graceful shutdown processes to ensure data integrity and minimal disruption
1. synchronizing its configuration with ZooKeeper, allowing seamless integration and accessibility by external scheduler

# How to test locally

1. start docker compose
1. install deps with `poetry install`
1. install scrapy project with `cd example & python setup.py install`
1. start the app with `python -m node_runner`
1. send `{"id": "uniq-id-1", "project": "testproject", "spider": "quotes", "spider_args": {}}` to `http://localhost:8000/start`

Note: This document is subject to further updates.
