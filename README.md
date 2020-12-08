# SE575_group14

Special thanks to Daniel Van Flymen (https://github.com/dvf) for his "Learn Blockchains by Building One" tutorial. 

Dependencies are:

    Flask v0.12.2
    
    Requests v2.18.4
    
    Python v3.8.6
    
    Node.js v10.23.0
    
    Npm v5.6.0
    
To install Flask and requests, you can use the following pip command:

    $ pip install Flask==0.12.2 requests==2.18.4 
   
Before running the client side, you need to run the server side. To run the server-side, simply run the blockchain.py file in either cmd or a code editor such as VS Code.

If you are using cmd, then change your directory to the one containing the "blockchain.py" file, and then write the following command:

    $ python3 blockchain.py
    
After running the sever-side you will see a message saying:

    * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)

There are multiple ways to run the client side, the most easiest and interactive is the with a web browser. To do that, locally open the URL port on any browser (we tested on chrome):
 
    http://127.0.0.1:8080/ or http://localhost:8080/

After opening the localhost, you can see your address. That address is unique to only you.
