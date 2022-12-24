function SendEmail(){
    email = document.getElementById("id_email").value
    var reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;
    if(reg_email.test(email)){                            
        const loader = document.getElementById("page-loader").classList = "show";
    }else {                       
        return false;         
    }
}