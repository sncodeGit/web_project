# auth.css BEGIN

auth_css = '''
<style>

body {
         display: flex;
         justify-content: center;
         align-items: center;
         height: 100vh;
 }
 
a {
         text-decoration: none;
         border-bottom: 3px solid #0071f0;
         color: black;
}
 
.form {
         width: 300px;
         padding: 32px;
         border-radius: 10px;
         box-shadow: 0 4px 16px #ccc;
         font-family: sans-serif;
         letter-spacing: 1px;
 }
 
.form_title { 
         text-align: center; 
         font-weight: normal;
 }
 
.form_button {
         padding: 10px 20px;
         font-family: sans-serif;
         letter-spacing: 1px;
         font-size: 16px;
         color :#fff ;
         background-color: #0071f0;
         cursor: pointer;
 }

.form_grup {
         position: relative;
         margin-bottom: 20px;
}

.form_input {
         width: 100%;
         padding: 0 0 10px 0;
         border: none;
         border-bottom: 1px solid #e0e0e0;
         background-color: transparent;
         outline: none;
 }
 
.form_label {
         position: absolute;
         z-index: -1;
         transition: 0.3s;
         top: -18px;
         font-size:12px;
         color: #e0e0e0;
 }
 
.g-signin2{
         margin-top: 5px;
         margin-left: 1px;
}

.form_input:focus {
         border-bottom: 1px solid #1a73a8;
 }
 
</style>
'''

# auth.css END
