export class LoginJsFunctions {
    constructor() { }
}

export class RegisterJsFunctions {
    constructor() { }
}

export class ArticleJsFunctions {
    constructor() { }
}

// common functions
export class CommonJsFunctions {
    constructor() { }

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
        // type -> "success","error","info","warning"
        $.toast({
            heading: this.capitalizeFirstLetter(type),
            text: message,
            icon: type,
            loader: true,        // Change it to false to disable loader
            loaderBg: '#9EC600',  // To change the background
            position: 'top-right',
        });
    }

    capitalizeFirstLetter(string) {
        return string ? string.charAt(0).toUpperCase() + string.slice(1) : '';
    }

    performPostAPICall(apiURL, method, data, dataType, processingButton,
        postProcessing, showSuccessMessage) {
        let originalButtonHtml = $(processingButton).html();
        $(processingButton).prop('disabled', true);
        $(processingButton).html('Processing...');

        $.ajax({
            type: method,
            url: apiURL,
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrfToken"]').attr('content')
            },
            contentType: dataType == 'json' ? 'application/json' : false,
            data: data,
            success: function (response) {
                $(processingButton).prop('disabled', false);
                $(processingButton).html(originalButtonHtml);
                if (response.status) {
                    if (showSuccessMessage) {
                        $.toast({
                            heading: 'Success',
                            text: response.message,
                            icon: 'success',
                            loader: true,        // Change it to false to disable loader
                            loaderBg: '#9EC600',  // Change it to false to disable loader
                            position: 'top-right',
                            afterHidden: postProcessing(response.data)
                        });
                    } else {
                        postProcessing(response.data);
                    }
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
            error: function (xhr, status, error) {
                $(processingButton).prop('disabled', false);
                $(processingButton).html(originalButtonHtml);
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

    fetchSelect2Data(url, placeholderText, minimumInputLength, extra_params) {
        console.log("extra_params: ", extra_params);
        return {
            ajax: {
                url: url,
                data: function (params) {
                    return Object.assign({}, {
                        // q: params.term, // search term
                        page: params.page || 1
                    }, extra_params);
                },
                dataType: 'json',
                processResults: function (data, params) {
                    params.page = params.page || 1;
                    return {
                        results: data.data,
                        pagination: {
                            more: (params.page * 10) < data.count
                        }
                    };
                },
                cache: true
            },
            placeholder: placeholderText,
            minimumInputLength: minimumInputLength,
        }
    }
}