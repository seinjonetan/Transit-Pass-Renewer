# Upass Renewer

Automatically renew your BC Translink Upass every month by scheduling this script on your computer, and never have an awkward moment again while tapping your card on the bus.

Currently compatible with UBC and SFU authentication portals.

## Getting Started

Clone the project:
```
git clone git@github.com:<your_github_username>/upass_renewer.git
```

### Prerequisites

* Python 3.5+
* Google Chrome

Use pip install to get other requirements:
```
pip install -r requirements.txt
```

## Setup and Scheduling

### Fill in config file

Enter your university name and authentication details into the config.yml file. Currently Upass Renewer only supports UBC and SFU authentication portals. For security reasons, please keep your config file in a safe location and never share it. Here's an example:

```
university: "University of British Columbia"
username: johnsmith
password: 0Tw22dzp0D
```

### Running the script

Run the script from your command line to check if it works. If your Upass is not available to renew, the script will simply halt after authentication.

```
python main.py
```

### Scheduling the script

There are several ways to do this, and can vary depening on your OS. Here are some helpful tutorials:

[Windows tutorial](https://www.esri.com/arcgis-blog/products/product/analytics/scheduling-a-python-script-or-model-to-run-at-a-prescribed-time/)
[Mac OS tutorial](https://www.maketecheasier.com/use-launchd-run-scripts-on-schedule-macos/)
[Linux tutorial](http://1selfsolutions.com/scheduling-python-script-linux-cron-job/)

## Acknowledgments

* Shoutout to Pvakil, whose code I based this project on
