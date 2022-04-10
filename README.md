<div id="top"></div>

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/bk62/polygon-scan-python">
    <!-- <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
  </a>

<h3 align="center">polygon-scan-python</h3>

  <p align="center">
    An API client for Polygon Scan written in python
    <br />
    <!-- <a href="https://github.com/bk62/polygon-scan-python"><strong>Explore the docs »</strong></a> -->
    <!-- <br /> -->
    <!-- <br /> -->
    <!-- <a href="https://github.com/bk62/polygon-scan-python">View Demo</a> -->
    <!-- · -->
    <a href="https://github.com/bk62/polygon-scan-python/issues">Report Bug</a>
    ·
    <a href="https://github.com/bk62/polygon-scan-python/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#references">References</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

An API client library for Polygon Scan written in Python 3

WIP

<!-- Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `bk62`, `polygon-scan-python`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `Polygon Scan Python `, `An API client for Polygon Scan written in python` -->

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

- [Requests](https://docs.python-requests.org/en/latest/)
- [poetry](https://python-poetry.org/)
- [pytest](https://docs.pytest.org/)
- [Betamax](https://github.com/betamaxpy/betamax)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Install poetry as in [https://python-poetry.org/docs/](https://python-poetry.org/docs/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/bk62/polygon-scan-python.git
   ```
2. Install required python packages with poetry
   ```sh
    cd polygon-scan-python
    poetry install
   ```
3. (Optional) Get a free API Key at [https://polygonscan.com](https://polygonscan.com)
4. (Optional) Enter your API KEY in an `.env` file
   ```sh
   echo "export POLYGON_SCAN_API_KEY=<YOUR_API_KEY>" > .env;
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

```python
  from polygon_scan import PolygonScan

  address = "0x157B46dF4457ee4aca3137950a2E412EF368C58B"

  pg_scan = PolygonScan()

  balance = pg_scan.account.get_account_balance(address)
  print(f"{address} balance: {balance}")

  txns = pg_scan.account.get_account_normal_transactions(address)
  for txn in txns[:5]:
    print(txn)
```

<!-- _For more examples, please refer to the [Documentation](https://example.com)_ -->

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [ ] Implement modules and methods for all API calls
- [ ] Handle PolygonScan errors - [https://docs.polygonscan.com/support/common-error-messages](https://docs.polygonscan.com/support/common-error-messages)
- [ ] Http client tests
- [ ] Documentation
  - [ ] Docstrings
  - [ ] Sphinx
- [ ] Pypi

See the [open issues](https://github.com/bk62/polygon-scan-python/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

This projet uses Betamax to mock requests by recording actual HTTP responses. The first time you add test an API call method:

1. Export `POLYGON_SCAN_API_KEY` from a `.env` file (refer to `.env.example`)
2. Run the `run_tests.sh` script which instructs Betamax to record response fixtures using the API key. The script also sets a 2 sec delay between requests to safely respect rate limits.
3. Delete the relevant fixture file `tests/fixtures/cassettes/test.<test_module_name>.<test_name>` if necessary.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

MIT

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

[@bk_862](https://twitter.com/bk_862)

Project Link: [https://github.com/bk62/polygon-scan-python](https://github.com/bk62/polygon-scan-python)

<p align="right">(<a href="#top">back to top</a>)</p>

## References

[PolygonScan docs](https://docs.polygonscan.com)

HTTP client implementation significantly influenced by [prawcore](https://github.com/praw-dev/prawcore)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/bk62/polygon-scan-python.svg?style=for-the-badge
[contributors-url]: https://github.com/bk62/polygon-scan-python/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bk62/polygon-scan-python.svg?style=for-the-badge
[forks-url]: https://github.com/bk62/polygon-scan-python/network/members
[stars-shield]: https://img.shields.io/github/stars/bk62/polygon-scan-python.svg?style=for-the-badge
[stars-url]: https://github.com/bk62/polygon-scan-python/stargazers
[issues-shield]: https://img.shields.io/github/issues/bk62/polygon-scan-python.svg?style=for-the-badge
[issues-url]: https://github.com/bk62/polygon-scan-python/issues
[license-shield]: https://img.shields.io/github/license/bk62/polygon-scan-python.svg?style=for-the-badge
[license-url]: https://github.com/bk62/polygon-scan-python/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
