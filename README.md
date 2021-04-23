# BT4222_repo

**Bitcoin Day Trading Using Machine Learning and Natural Language Processing** 

With the observation that cryptocurrency prices are heavily influenced by sentiments because they do not have sophisticated real life use cases, coupled with attempts from researchers to incorporate sentiment analysis into machine learning prediction, this project aims to investigate the usefulness of sentiment analysis on Bitcoin day trading on small data sets.

There are a total of five data sources used in this project:
1. Bitcoin-related price information (adjusted close bitcoin price, bitcoin volume, e.g.) extracted from [Yahoo Finance](https://sg.finance.yahoo.com/)
2. Macroeconomic factors such as S&P 500 Price, Gold Price and Global Currency Ratios (CHF, EUR, GBP, JPY, CNY  against the US dollar) extracted from [Yahoo Finance](https://sg.finance.yahoo.com/)
3. Blockchain information (transactions per block and blockchain hash rates) extracted from [Blockchain.com](https://www.blockchain.com/)
4. Daily Top 50 Reddit Post and Reddit Comment  Sentiments from [Reddit](https://www.reddit.com/)
5. CoinDesk Article Sentiments and volume of posts from [CoinDesk](https://www.coindesk.com/)

## Setup

1) Create a [virtual environment](https://docs.python.org/3/library/venv.html) within your project directory.

Conda
```bash
conda create -n myenv pip
```
Pip
```bash
python3 -m venv /path/to/new/virtual/environment
```

2) Activate the virtual environment in your project directory in your terminal 

Conda
```bash
conda activate myenv
```

Pip
```
$ C:\Users\...\project_folder> venv\Scripts\activate
```

3) Clone repository:
```bash
git clone https://github.com/YangYuesong0323/BT4222_repo.git
```

4) Install the required packages
```bash
pip install -r requirements.txt --upgrade
```

## Info
Group Project for NUS BT4222 Module </br>
Done by: Group 15 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
