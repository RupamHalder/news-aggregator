export class LoginJsFunctions {
    constructor() {}
}

export class RegisterJsFunctions {
    constructor() {}

    registerUser(registerButton) {
        $(registerButton).prop('disabled', true);
        $(registerButton).html('Registering...');

        $.ajax({
            type: 'POST',
            url: '/api/v1/user/register',
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrfToken"]').attr('content')
            },
            contentType: 'application/json',
            data: JSON.stringify({
                email: $('#email').val(),
                password: $('#password').val(),
                conf_password: $('#conf_password').val()
            }),
            success: function(response) {
                $(registerButton).prop('disabled', false);
                $(registerButton).html('Register');
                if (response.status) {
                    $.toast({
                        heading: 'Success',
                        text: response.message,
                        icon: 'success',
                        loader: true,        // Change it to false to disable loader
                        loaderBg: '#9EC600',  // Change it to false to disable loader
                        position: 'top-right',
                        afterHidden: function () {
                            window.location.href = '/login';
                        }
                    });
                } else {
                    $.toast({
                        heading: 'Error',
                        text: response.message,
                        icon: 'error',
                        loader: true,        // Change it to false to disable loader
                        loaderBg: '#9EC600',  // Change it to false to disable loader
                        position: 'top-right'
                    });
                }
            },
            error: function(xhr, status, error) {
                $(registerButton).prop('disabled', false);
                $(registerButton).html('Register');
                $.toast({
                    heading: 'Error',
                    text: xhr.responseJSON.message,
                    icon: 'error',
                    loader: true,        // Change it to false to disable loader
                    loaderBg: '#9EC600',  // Change it to false to disable loader
                    position: 'top-right'
                });
            }
        });
    }
}

// common functions
export class CommonJsFunctions {
    constructor() {}

    togglePasswordVisibility(toggleElement) {
        if ($(toggleElement).find('i').attr("class") == "bi bi-eye") {
            $(toggleElement).find('i').attr("class", "bi bi-eye-slash");
            $(toggleElement).prev('input').attr("type", "password");
        }
        else if ($(toggleElement).find('i').attr("class") == "bi bi-eye-slash") {
            $(toggleElement).find('i').attr("class", "bi bi-eye");
            $(toggleElement).prev('input').attr("type", "text");
        }
    }

    showCommingSoon() {
        $.toast({
            heading: 'Comming soon...',
            text: 'This feature is comming soon.',
            icon: 'info',
            loader: true,        // Change it to false to disable loader
            loaderBg: '#9EC600',  // To change the background
            position: 'top-right',
        });
    }

    showMessage(message, type) {
        $.toast({
            text: message,
            icon: type,
            loader: true,        // Change it to false to disable loader
            loaderBg: '#9EC600',  // To change the background
            position: 'top-right',
        });
    }
}