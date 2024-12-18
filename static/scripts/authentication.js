
const LoginButton = document.getElementById('LoginButton');
const LoginModal = new bootstrap.Modal(document.getElementById('LoginModal'));
const RegisterButton = document.getElementById('RegisterButton');
const Registermodal = new bootstrap.Modal(document.getElementById('RegisterModal'));

LoginButton.addEventListener('click', function() {
    LoginModal.show();
});


function showLoginModal() {
    const LoginModal = new bootstrap.Modal(document.getElementById('LoginModal'));
    LoginModal.show();
}





RegisterButton.addEventListener('click', function() {
    Registermodal.show();
});



  function showRegisterModal() {
    const LoginModal = new bootstrap.Modal(document.getElementById('LoginModal'));
    LoginModal.show();
}