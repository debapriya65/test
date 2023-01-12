function myFunction() {
    const text=document.getElementById('textarea').value ;
    document.getElementById('textarea').value ="";
    const json={
        "name":text,
    }
    const dialog2=document.getElementById("dialog2");
    const dialog=document.querySelector("dialog");
    dialog2.innerHTML=`
    <h1>Loading</h1>
    <div class="loader"></div>
    <button id="hide">Close</button> 
    `
    document.getElementById('hide').onclick = function() {    
        dialog.close();    
    };
    document.querySelector(".loader").style.visibility = "visible";
    dialog.show();
    const xhr = new XMLHttpRequest();
    xhr.open("POST","http://127.0.0.1:5000/predict_api");
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = () => {
        let data = xhr.response;
        document.querySelector(".loader").style.visibility = "hidden";
        console.log(data)
        dialog2.innerHTML=(`<p>\n \n`+data+`</p><button id="hide">Close </button>  `);
        document.getElementById('hide').onclick = function() {    
            dialog.close();    
        };
        console.log(data);
        }
    xhr.send(JSON.stringify(json));
    
}