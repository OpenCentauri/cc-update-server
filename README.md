Docker compose example:

```yml
services:
  update-server:
    image: ghcr.io/opencentauri/cc-update-server:latest
    restart: unless-stopped
    environment:
      - ENCRYPTION_KEY=78B6A614B6B6E361DC84D705B7FDDA33C967DDF2970A689F8156F78EFE0B0928
      - ENCRYPTION_IV=54E37626B9A699403064111F77858049
      - HOST=https://u.opencentauri.cc
    ports:
      - 5515:5000
networks: {}
```