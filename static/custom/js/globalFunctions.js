export class LoginJsFunctions {
    constructor() {}
}

export class RegisterJsFunctions {
    constructor() {}
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
}