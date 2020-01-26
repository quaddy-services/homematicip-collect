
Based on

<https://github.com/coreGreenberet/homematicip-rest-api>

collect all hidden values from the Homematic IP devices via API

# Install

* Install <https://www.python.org/downloads/>
* Run `pip install -U homematicip`
* Run `python hmip_generate_auth_token.py`
(generates a config.ini)

Regulary run
`python collect_values.py`
(e.g. via repeating Scheduled Tasks)

and for each Heating-Group a .csv file (tab-seperated) will be created containing

* Date
* Actual temperature
* Actual Humidity
* For each Heating component:
* * Requested temperature
* * Valve Position

| date	| actual	| humidity	| set	| valve |
| ------------- | ------------- | ------------- | ------------- |
| 2020-01-23 07:54:08.930493	| 20,2	| 47	| 19	| 0 |
| 2020-01-23 07:59:08.451699	| 20,2	| 47	| 19	| 0 |
| 2020-01-23 08:04:08.652793	| 20,2	| 47	| 21,5	| 51 |
