$(document).ready(function(){
	$("#createContact").click(function(){
		$("#newContact").dialog({
			modal:true,
			width:500,
			height:350,
			buttons:[{"text":"Add",click:addContact()},{"text":"cancel",click:function(){$("#newContact").dialog( "close" );}}],
		});
	});
});

//$("#newContact").dialog();
function addContact(){
	var firstName = $("#firstName").val();
	var lastName = $("#lastName").val();
	var email = $("#email").val();
	var mobile = $("#mobile").val();
	var alternateNumber = $("#alternateNumber").val();
	if(!firstName || (jQuery.trim( firstName )).length==0){
		$("#addWarning").html("First Name Cannot be Empty");
		return false;
	}
	if(!mobile || (jQuery.trim( mobile )).length==0){
		$("#addWarning").html("Mobile Number Cannot be Empty");
		return false;
	}
	if(mobile.length>10){
		$("#addWarning").html("Mobile number length should not exceed 10 numbers");
		return false;
	}
	if(email){
		if(!validateEmail(email)){
			$("#addWarning").html("Email entered is not a valid one");
			return false;
		}
	}
}

function checkSignUpForm(){
	var email = $("#email").val();
	var password = $("#password").val();
	var confirmPassword = $("#confirmPassword").val();
	if(!email){
		$("#warning").html("Please Enter your Email");
		return false;
	}
	console.log(email);
	
	if(!password){
		$("#warning").html("Please Enter your password");
		return false;
	}
	if(!confirmPassword){
		$("#warning").html("Please Enter Confirm password");
		return false;
	}
	var testEmail = email.indexOf(" ");
	var testPassword = password.indexOf(" ");
	var testConfirmPassword = confirmPassword.indexOf(" ");
	if(!validateEmail(email)){
		$("#warning").html("Please Enter valid Email");
		return false;	
	}
	if(testEmail!=-1){
		
		$("#warning").html("Email cannot contain spaces");
		return false;
	}
	if(testPassword!=-1){
		$("#warning").html("Password cannot contain spaces");
		return false;
	}
	if(password.length<6){
		$("#warning").html("Password length cannot be less than 6 characters");
		return false;	
	}
	if(testConfirmPassword!=-1){
		$("#warning").html("Confirm Password cannot contain spaces");
		return false;
	}
	
	
	if(password!=confirmPassword){
		$("#warning").html("Confirm Password did not matched with password field");
		return false;
	}
	
	
}

function validateEmail(email) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}
