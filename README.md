# top-pypi-packages

A web page with the most-downloaded packages from PyPI:

* https://robert-96.github.io/top-pypi-packages/

A dump of the 5,000 most-downloaded packages from PyPI (including summary, keywords, version and license):

* https://robert-96.github.io/top-pypi-packages/json/packages.json

![Screenshot](/screenshots/screenshot.png)

> **Note**: This package expends the list from https://github.com/hugovk/top-pypi-packages with the package info from the PyPI API.


## Development

### Setup

Use the following command to install all dependencies:

```
$ pip install -r requirements.txt
```

### Serve

```
$ python -m scripts
```

Will start a dev server on http://localhost:8080/.

### Build

Run the following command to build the project:

```
$ python -m scripts.build
```

You can find the build inside the `dist/` directory.

### Test

You can run install the dev dependencies using the following command:

```
$ pip install -r requirements-dev.txt
```

You can run the tests using the following command:

```
$ pytest tests
```

## License

This project is licensed under the [MIT License](LICENSE).
