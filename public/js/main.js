function toogle_transaction(){
    document.getElementById("make_transaction").style.visibility = "visible";
    document.getElementById("toggle_transaction").style.visibility = "hidden";
}

function make_transaction(sender,recipient,amount){
    if (sender == recipient){
        Swal.fire({
            type: 'error',
            title: 'Sender cannot be the reciever',
          })
    }
    if (recipient.length == 0 || !recipient.replace(/\s/g, '').length){
        Swal.fire({
            type: 'error',
            title: 'Invalid input for Recipient!',
        })
    }
    if (isNaN(amount) || amount.length == 0 || !amount.replace(/\s/g, '').length){
        Swal.fire({
            type: 'error',
            title: 'Invalid Input, Amount needs to be an integer!',
        })
    }
    var obj = { sender: sender, recipient: recipient, amount: amount };
    var success= false;
    fetch('/new_transaction',{
        method: 'POST',
        body: JSON.stringify(obj)
    })
    .then(function (response) {
        return response.json();
    }).then(function (text) {
        
        if(text["message"] == "Sender does not have sufficient balance to make transaction, sender has either already sent all the currency or it is in process"){
            document.getElementById("toggle_transaction").style.visibility = "visible";
            document.getElementById("make_transaction").style.visibility = "hidden";
            document.getElementById("recipient").value="";
            document.getElementById("amount").value="";
            document.getElementById("output").innerHTML="";
            Swal.fire({
                type: 'error',
                title: 'Sender does not have sufficient balance to make transaction, sender has either already sent all the currency or it is in process',
            });
        }
        else{
            success = true;
            runningbal();
            document.getElementById("toggle_transaction").style.visibility = "visible";
            document.getElementById("make_transaction").style.visibility = "hidden";
            document.getElementById("recipient").value="";
            document.getElementById("amount").value="";
            document.getElementById("output").innerHTML="";
            Swal.fire({
                type: 'success',
                title: text["message"],
            });
        }
        // else{
        //     document.getElementById("toggle_transaction").style.visibility = "visible";
        //     document.getElementById("make_transaction").style.visibility = "hidden";
        //     document.getElementById("recipient").value="";
        //     document.getElementById("amount").value="";
        //     Swal.fire({
        //         type: 'error',
        //         title: 'Sender does not have sufficient balance to make transaction, sender has either already sent all the currency or it is in process',
        //     });

        // }
    });
}

function toogle_edit(){
    document.getElementById("make_edit").style.visibility = "visible";
    document.getElementById("toggle_edit").style.visibility = "hidden";
}

function make_edit(blockno,proof){
    if (isNaN(blockno) || blockno.length == 0 || !blockno.replace(/\s/g, '').length){
        Swal.fire({
            type: 'error',
            title: 'Invalid input for Block Number! (Needs to be an integer)',
        })
    }
    else if (isNaN(proof) || proof.length == 0 || !proof.replace(/\s/g, '').length){
        Swal.fire({
            type: 'error',
            title: 'Invalid input for Proof! (Needs to be an integer)',
        })
    }
    else{
        var obj = { blockno: blockno, proof: proof};
        var data;
        var success= false;
        fetch(`/edit`,{
            method: 'POST',
            body: JSON.stringify(obj)
        })
        .then(function (response) {
            return response.text();
        }).then(function (text) {
            data = text; 
            if (text == "Block number does not exist!"){
                document.getElementById("toggle_edit").style.visibility = "visible";
                document.getElementById("make_edit").style.visibility = "hidden";
                document.getElementById("blockno").value="";
                document.getElementById("proof").value="";
                document.getElementById("output").innerHTML="";
                Swal.fire({
                    type: 'error',
                    title: 'Block number does not exist!',
                })
            }
            if (text == "Invalid input for Proof! (Needs to be an integer)"){
                document.getElementById("toggle_edit").style.visibility = "visible";
                document.getElementById("make_edit").style.visibility = "hidden";
                document.getElementById("blockno").value="";
                document.getElementById("proof").value="";
                Swal.fire({
                    type: 'error',
                    title: 'Invalid input for Proof! (Needs to be an integer)',
                })
            }
            else{
                success = true;
                console.log("SSS");
                document.getElementById("output").innerHTML = text;
                if (success==true){
                    document.getElementById("toggle_edit").style.visibility = "visible";
                    document.getElementById("make_edit").style.visibility = "hidden";
                    document.getElementById("blockno").value="";
                    document.getElementById("proof").value="";
                }
            }
            
        
        });
    }
}

function mine(){
    var data;
    fetch(`/mine`)
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        document.getElementById("output").innerHTML = text;
        runningbal(); 
    });
}

function runningbal(){
    fetch(`/spend`)
    .then(function (response) {
        return response.json();
    }).then(function (text) {
        var x = document.createElement("TABLE");;
        x.setAttribute('border','1');
        var tr1 = document.createElement("tr");
        var td1 = document.createElement("td");
        var td2 = document.createElement("td");
        td1.appendChild(document.createTextNode("Address"));
        td2.appendChild(document.createTextNode("Balance"));
        // for (var i =0 ;i<text.length;i++){
        tr1.appendChild(td1);
        tr1.appendChild(td2);
        x.appendChild(tr1);
        // }
        for (var key in text) {
            // check if the property/key is defined in the object itself, not in parent
            if (text.hasOwnProperty(key)) {           
                td1 = document.createElement("td");
                td1.append(key);
                td2 = document.createElement("td");
                td2.append(text[key]);
                tr1 = document.createElement("tr");
                tr1.appendChild(td1);
                tr1.appendChild(td2);
                x.appendChild(tr1);
            }
        }
        document.getElementById("transactions").innerHTML = "";
        document.getElementById("transactions").appendChild(x); 

    });
}