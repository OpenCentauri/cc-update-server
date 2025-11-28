Docker compose example:

```yml

services:
    update-server:
        image: ghcr.io/OpenCentauri/cc-update-server:latest
        restart: unless-stopped
        environment:
            - ENCRYPTION_KEY=ABCDEF
            - ENCRYPTION_IV=ABCDEF
        ports:
            - 5515:5000

```