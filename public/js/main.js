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
    var data;
    var success= false;
    fetch(`/new_transaction`,{
        method: 'post',
        body: JSON.stringify(obj)
    })
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('POST response text:');
        data = text; 
        success = true
    });
    if (success==true){
        document.getElementById("toggle_transaction").style.visibility = "visible";
        document.getElementById("make_transaction").style.visibility = "hidden";
    }
    console.log(data);
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
    if (isNaN(proof) || proof.length == 0 || !proof.replace(/\s/g, '').length){
        Swal.fire({
            type: 'error',
            title: 'Invalid input for Proof! (Needs to be an integer)',
        })
    }

    var obj = { blockno: blockno, proof: proof};
    var data;
    var success= false;
    fetch(`/edit`,{
        method: 'post',
        body: JSON.stringify(obj)
    })
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        data = text; 
        if (data == "Block number does not exist!"){
            Swal.fire({
                type: 'error',
                title: 'Block number does not exist!',
            })
        }
        else{
            success = true;
        }
    });
    if (success==true){
        document.getElementById("toggle_edit").style.visibility = "visible";
        document.getElementById("make_edit").style.visibility = "hidden";
    }
    console.log(data);

}

function mine(){
    var data;
    fetch(`/mine`)
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        data = text 
        console.log(data);
        console.log(text);
    });
    // console.log(data);
}

function chain(){
    var data;
    fetch(`/chain`)
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        data = text 
        console.log(data);
    });
}