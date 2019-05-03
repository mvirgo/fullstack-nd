function init() {
  gapi.load('auth2');
  if (gapi.auth2.getAuthInstance().isSignedIn.get()) {
    document.getElementById("googleOut").style.display="block";
    document.getElementById("authNeeded").style.display="block";
    document.getElementById("noAuth").style.display="none";
  } else {
    document.getElementById("googleIn").style.display="block";
    document.getElementById("authNeeded").style.display="none";
    document.getElementById("noAuth").style.display="block";
  }
}

function onSignIn(googleUser) {
  document.getElementById("googleOut").style.display="block";
  document.getElementById("googleIn").style.display="none";
  document.getElementById("authNeeded").style.display="block";
  document.getElementById("noAuth").style.display="none";
}

function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
  document.getElementById("googleIn").style.display="block";
  document.getElementById("googleOut").style.display="none";
  document.getElementById("authNeeded").style.display="none";
  document.getElementById("noAuth").style.display="block";
}