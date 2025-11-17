# API_SHOP

Run yarn or npm i to download package
Create new file .env
Copy value of .env-example and paste .env
Run yarn initDB or npm initDB init database
Run yarn start or npm start to run server

npm run start

# Datasheet (MongoDB)

run command in shell to dump data into mongodb:

```bash
mongodump --db test --archive="$(pwd)/backup_test.gz" --gzip
```

run command in shell to restore data into mongodb:

```bash
mongorestore --host (your_host) --port (your_port) --db test --archive="$(pwd)/restore.gz" --gzip
```
