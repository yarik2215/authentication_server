# authentication_server

### Migrations
For initalizing aerich use:
```
aerich init -t app.settings.TORTOISE_ORM
```

For initalizing a db use:
```
aerich init-db
```

For making migrations use:
```
aerich migrate
```

For applying migrations use:
```
aerich upgrade
```
<hr>

## Running localy

For run project loccaly
1. Create `.env` file
2. Install packages with pipenv `pipenv install`
3. Apply migrations `pipenv run migrate`
4. Run app using `pipenv run start`
5. For running tests use `pipenv run test`