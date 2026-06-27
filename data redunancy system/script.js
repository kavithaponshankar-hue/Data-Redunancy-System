// Delete confirmation

function confirmDelete(){

    return confirm(
        "Are you sure you want to delete this record?"
    );

}


// Auto-hide flash messages

setTimeout(function(){

    let alerts=document.querySelectorAll(".alert");

    alerts.forEach(function(alert){

        alert.style.transition="0.5s";

        alert.style.opacity="0";

        setTimeout(function(){

            alert.remove();

        },500);

    });

},3000);


// Prevent empty spaces

document.addEventListener("DOMContentLoaded",function(){

    let inputs=document.querySelectorAll("input");

    inputs.forEach(function(input){

        input.addEventListener("blur",function(){

            this.value=this.value.trim();

        });

    });

});