Simple script to share your Thunderbird profile between multiple computers

## Motivation

Do you have more than one workstation ( PC,NB .... ) and do you want to keep your thunderbirds in sync ? This may be the
solution.

## Installation

* Install python3.4 +
* Install google drive REST API:

  * **Windows:**

   `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib hurry.filesize`

  * **Ubuntu 18.04 with venv :**

  `bash` - fish doesn't work

  `python3 -m venv venv`
  
  `source venv/bin/activate`

  `python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib hurry.filesize appdirs`

* Start using this script by launching main.py with otiopns

   `python main.py -a download # get latest backup`

   `python main.py -a upload # update backup from this device`

   `python main.py -a list # list curently availabla backup files`



## Contributors

for more info contact me via mail kecalcze@gmail.com

## License

MIT license
