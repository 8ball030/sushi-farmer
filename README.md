

<!-- ABOUT THE PROJECT -->
## About The Project

The project is simple sushi yield farmer. The application can be run locally and interacts with the Polygon chain.

### Built With

* [FetchAi](https://docs.fetch.ai/)
* [SushiSwap](https://sushi.com/)
* [Polygon/MATIC](https://polygon.technology/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* First generate a fresh ethereum address for testing on polygon/matic
* Retrieve the 24 word nmonic backup phrase
* load the wallet with Matic from Polygon
* Navigate to Sushi.com
* Check out the /farms to decide what yield you want to harvest
* Swap into these pairs
* provide liquidity
* head to farms and stake your LP token.



### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/8ball030/sushi-farmer.git
   ```
2. Install packages & write private key to file
   ```sh
   pipenv run install
   ```



<!-- USAGE EXAMPLES -->
## Usage
The auto harvester has a number of configurable parameters available in /skills/harvester/skill.yaml

Config these parameters 

- service_interval = time in seconds as to how frequently the harvest is performed.
- min_sushi = minimum sushi after which to collect yield. (In gwei) 

```
pipenv run agent
```


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/8ball030/sushi-farmer/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact


[Link](https://github.com/8ball030/sushi-farmer])


