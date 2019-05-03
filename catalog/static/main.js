function init() {
  /*
  Shows or hides Google Sign-In and authentication-related messages
  when page loads based on whether they are signed in or not.
  */
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
  /*
  Shows sign out link and content for only authenticated users,
  while hiding the Google Sign In button and any content
  that mentions the need to sign in.
  */
  document.getElementById("googleOut").style.display="block";
  document.getElementById("googleIn").style.display="none";
  document.getElementById("authNeeded").style.display="block";
  document.getElementById("noAuth").style.display="none";
}

function signOut() {
  /*
  Signs out the user, then displays the Google Sign In button,
  along with any messages discussing the need to sign in
  for any related features. Also, hides the sign out link,
  as well as hiding any features that require authentication.
  */
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
  document.getElementById("googleIn").style.display="block";
  document.getElementById("googleOut").style.display="none";
  document.getElementById("authNeeded").style.display="none";
  document.getElementById("noAuth").style.display="block";
}