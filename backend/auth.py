from __future__ import print_function
import json
#  from google.auth.transport import requests
#  from google.oauth2 import id_token

def lambda_handler(event, context):
    # TODO implement
    ret = {}
    ret['statusCode'] = 200
    ret['headers'] = {
        'Content-Type': 'text/html'
    }

    google_token = "1069669795497-ifvno18k8plqe1rdumnjls437oehl0ke"
    api_url = "https://jx979dbwxe.execute-api.us-east-1.amazonaws.com/prod" 

    google_login_page = f'''
    <html lang="en">
      <head>
        <meta name="google-signin-scope" content="profile email">
        <meta name="google-signin-client_id" 
          content="%s.apps.googleusercontent.com">
        <script src="https://apis.google.com/js/platform.js" async defer></script>
      </head>
      <body>
        <div class="g-signin2" data-onsuccess="onSignIn" data-theme="dark"></div>

        <form action="./prod" method="get">
          <input type="hidden" name="lol" value="1">
          <textarea name="kek" cols="50" rows="40" id="tokenField">No token provided: Sign in first</textarea>
          <br>
          <input type="submit" value="Login with this token">
        </form>


        <script>
          var kek = 0
          function onSignIn(googleUser) {{
            // Useful data for your client-side scripts:
            kek = kek + 1;
            console.log("Kek is " + kek)
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

            document.getElementById("tokenField").innerHTML = id_token;
     
            var request = new XMLHttpRequest();
            request.open("GET","%s", true);
            request.setRequestHeader("Authorization", id_token);
            request.onload = function() {{
              //googleUser.isSignedIn();
              var text = request.responseText;
              document.getElementById("tokenField").innerHTML = id_token;
            }};
            request.send(); 

          }}
          function signOut() {{
            var auth2 = gapi.auth2.getAuthInstance();
            auth2.signOut().then(function () {{
              console.log('User signed out.');
            }});
          }}
        </script>
      </body>
    </html>
    ''' % (google_token, api_url)
    ret['body'] = google_login_page
    return ret
