# Ape Pokt Plugin

Pokt Provider plugin for Ethereum-based networks.

## Dependencies

* [python3](https://www.python.org/downloads) version 3.7 or greater, python3-dev

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-pokt
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-pokt.git
cd ape-pokt
python3 setup.py install
```

## Quick Usage

First, make sure you have one of the following environment variables set (it doesn't matter which one):

* `WEB3_POKT_PROJECT_ID`
* `WEB3_POKT_API_KEY`

Either in your current terminal session or in your root RC file (e.g. `.bashrc`), add the following:
```
export WEB3_POKT_PROJECT_ID=MY_API_TOKEN
```
To use the Pokt provider plugin in most commands, set it via the `--network` option:
```
ape console --network ethereum:goerli:pokt
```
## Development

This project is in development and should be considered a beta.
Things might not be in their final state and breaking changes may occur.
Comments, questions, criticisms and pull requests are welcomed.

## License

This project is licensed under the [Apache 2.0](LICENSE).
