# Price Updater #
This repository contains the source code for both the backend and the mobile app. It's used to update products price of and old program's DBF File (DBase/Foxpro), using a mobile android device to scan barcodes and update price.


## Structure  
- `/backend` - Contains the backend code built with Python and Flask. Note that the code is written in Python 2 for compatibility reasons, as it is intended to run on a server that uses it for other applications, but it can be ported to Python 3 with some minor changes.
- `/mobile` - Contains the mobile app code built with NativeScript Vue.  


## Installation ##

   1. Clone the repository:  
      ```bash
      git clone https://github.com/flaviobovio/act_precios.git  
      cd act_precios

   2. Backend
      In the backend folder

      config.ini stores backend configuration

      Using a Python 2 Virtual Enviroment
      ```bash
      python -m venv venv  
      source venv/bin/activate  
      pip install -r requirements.txt
      waitress-server app:app
      ```

      Using Docker
      ```bash
      docker build -t python2-bash .
      docker run -it -v .:/app -p 8080:8080 python2-bash
      ```

   3. Mobile
      In the mobile folder

      Install NativeScript Vue
      Refer to https://nativescript-vue.org/en/docs/introduction/ for instructions

      Aditional plugins requiered
      - @fortawesome/fontawesome-free@6.2
      - @nstudio/nativescript-barcodescanner@5.0.1
      - dotenv@16.4.



