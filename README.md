# SE575_group14

Code is based on Daniel Van Flymen's (https://github.com/dvf) "Learn Blockchains by Building One" tutorial. 

Dependencies are Flask and Requests, which can be installed by

    pip install flask
and 

    pip install requests

Then, the program can be run with

    python blockchain.py
    
which opens locally on port http://127.0.0.1:5000/. This can be reached using Postman or some other API service at http://localhost:5000/.

Using an API service, the possible interactions are:

    http://localhost:5000/chain
    
Which uses the GET option to view the current state of the blockchain,

    http://localhost:5000/mine
    
Which uses the GET option to add a new block to the chain, and

    http://localhost:5000/transactions/new
    
Which uses the POST option to record a new transaction. This also requires an entry in the body, with the form

    {
      "sender": [my address],
      "recipient" : [receiver's address],
      "amount" : [amount to send]
    }

