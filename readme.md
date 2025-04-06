# Setup

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Install ["Data Wrangler"](https://code.visualstudio.com/docs/datascience/data-wrangler#_launch-data-wrangler-directly-from-a-file) extension to visualize `.csv`

# Execute
1. Edit `VISUALIZE` variable in `main.py`, if you want to visualize algorithm "decisions" 
2. `make` or `python3 main.py`
3. Right-click on `solutions.csv` and select `Open in Data Wrangler"