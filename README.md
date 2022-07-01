# top-pypi-packages

A web page with the most-downloaded packages from PyPI:

* https://robert-96.github.io/top-pypi-packages/

You can also download a dump of the 5,000 most-downloaded packages from PyPI (including summary, keywords, version and license):

* https://robert-96.github.io/top-pypi-packages/json/packages.json

![Screenshot](/screenshots/screenshot.png)

## Development

### Setup

```
$ pip install -r requirements.txt
```

### Serve

```
$ python -m scripts
```

Will start a dev server on http://localhost:8080/

### Build

```
$ python -m scripts.build
```

### Test

```
$ pip install -r requirements-dev.txt
$ pytest tests
```

## License

This project is licensed under the [MIT License](LICENSE).
