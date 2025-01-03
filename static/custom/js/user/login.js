$(document).ready(function() {
    $(document).on('click', '#togglePassword', function(){
        togglePasswordVisibility();
    });
});

function togglePasswordVisibility(){
    if ($("#togglePassword i").attr("class") == "bi bi-eye") {
        $("#togglePassword i").attr("class", "bi bi-eye-slash");
        $("#password").attr("type", "password");
    }
    else if ($("#togglePassword i").attr("class") == "bi bi-eye-slash") {
        $("#togglePassword i").attr("class", "bi bi-eye");
        $("#password").attr("type", "text");
    }
}
