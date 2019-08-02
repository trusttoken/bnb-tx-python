# Development
Start by cloning the repository.
```
git clone git@github.com:trusttoken/bnb-tx-python.git
```

Install dependencies
```
pipenv install
```

Run flake8
```
pipenv run flake8
```

# Pull Requests
Please try to adhere to the following guidelines.

* Code should pass `flake8` linting
* New transaction types need testing of both amino and JSON encodings
