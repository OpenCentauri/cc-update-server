Docker compose example:

```yml
services:
  update-server:
    image: ghcr.io/opencentauri/cc-update-server:latest
    restart: unless-stopped
    environment:
      - ENCRYPTION_KEY=...
      - ENCRYPTION_IV=...
      - HOST=https://u.opencentauri.cc
    ports:
      - 5515:5000
networks: {}
```