Simple script to share your Thunderbird profile between multiple computers

## Motivation

Do you have more than one workstation ( PC,NB .... ) and do you want to keep your thunderbirds in sync ? This may be the
solution.

## Installation

* Install python3.4 +
* Install google drive REST API:

  * **Windows:**

   `pip install --upgrade google-api-python-client`

  * **Ubuntu 16.04+ :**

  `sudo apt-get install python3-setuptools`

  `sudo easy_install3 pip`

  `sudo pip3 install --upgrade google-api-python-client` 
    
    or
    
    ``apt install python3-googleapi``

* Start using this script by launching main.py with otiopns
   
   `python main.py -a download # get latest backup`

   `python main.py -a upload # update backup from this device`
   


## Contributors

for more info contact me via mail kecalcze@gmail.com

## License

MIT license
