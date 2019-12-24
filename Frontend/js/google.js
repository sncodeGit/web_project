function onSignIn(googleUser) {
    // Useful data for your client-side scripts:
    var profile = googleUser.getBasicProfile();
    console.log("ID: " + profile.getId()); // Don't send this directly to your server!
    console.log("Full Name: " + profile.getName());
    console.log("Given Name: " + profile.getGivenName());
    console.log("Family Name: " + profile.getFamilyName());
    console.log("Image URL: " + profile.getImageUrl());
    console.log("Email: " + profile.getEmail());
 
    // The ID token you need to pass to your backend:
    var id_token = googleUser.getAuthResponse().id_token;
    console.log("ID Token: " + id_token);
    
    var request = new XMLHttpRequest();
    request.open("GET","https://5v2mv5awy4.execute-api.us-east-1.amazonaws.com/default/post_test?a=b", false);
    request.setRequestHeader("Authorization", id_token);
    request.onload = function() {
      var text = request.responseText;
      document.getElementById("content").innerHTML = text;
    };
    request.send(); 
}
