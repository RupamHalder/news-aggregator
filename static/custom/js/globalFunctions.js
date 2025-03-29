export class LoginJsFunctions {
    constructor() { }
}

export class RegisterJsFunctions {
    constructor() { }
}

export class ArticleJsFunctions {
    constructor() { }

    genGetSourcesAPIRequest() {
        let language = $("#language").val();
        let country = $("#country").val();
        let category = $("#category").val();
        let otherParams = {}
        if (language != null) {
            otherParams.language = language;
        } if (country != null) {
            otherParams.country = country;
        } if (category != null) {
            otherParams.category = category;
        }
        return otherParams
    }

    loadArticlesFromData(articleData, isLoggedIn) {
        let articleDiv = $('#articleDiv');
        articleDiv.html(``);
        
        if (articleData.length == 0) {
            articleDiv.html(
                `
                    <div class="col-lg-12">
                        <div class="text-center">
                            <h2>No articles found</h2>
                        </div>
                    </div>
                `
            )
        } else {
            articleData.forEach(article => {
                const sentiment = article.sentiment; 
                let sentimentBadge = '';

                if (sentiment > 0.1) {
                    sentimentBadge = '<span class="badge bg-success">Positive</span>';
                } else if (sentiment < -0.1) {
                    sentimentBadge = '<span class="badge bg-danger">Negative</span>';
                } else {
                    sentimentBadge = '<span class="badge bg-secondary">Neutral</span>';
                }

                let saveArticleBtn = '';
                if (isLoggedIn) {
                    saveArticleBtn = `
                        <div class="d-inline">
                            <button
                                type="submit"
                                class="btn btn-primary btn-sm"
                                id="btnSaveArticle"
                                data-title="${article.title !== null ? article.title : ''}"
                                data-url="${article.title !== null ? article.url : ''}"
                                data-description="${article.title !== null ? article.description : ''}"
                                data-article_image_url="${article.title !== null ? article.urlToImage : ''}"
                                data-sentiment="${ article.sentiment }"
                                data-published_at="${ article.publishedAt }"
                            >
                                Save Article
                            </button>
                        </div>
                    `;
                }

                articleDiv.append(`
                    <div class="col my-3">
                        <div class="card h-100">
                            <img
                            src="${article.urlToImage}"
                            class="card-img-top"
                            alt="${article.title}"
                            />
                            <div class="card-body">
                            <h5 class="card-title">${article.title}</h5>
                            <p class="card-text">${article.description}</p>

                            <div class="sentiment-indicator mb-3">
                                ${sentimentBadge}
                            </div>

                            <a
                                href="${article.url}"
                                class="btn btn-secondary btn-sm"
                                target="_blank"
                                >Read More</a
                            >

                            ${saveArticleBtn}

                            </div>
                            <div class="card-footer">
                            <small class="text-muted"
                                >${ article.publishedAt.split('T')[0] }</small
                            >
                            </div>
                        </div>
                        </div>    
                `)
            });
        }
    }
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

    fetchSelect2Data(url, placeholderText, minimumInputLength, extraParams) {
        return {
            ajax: {
                url: url,
                data: function (params) {
                    return Object.assign({}, {
                        q: params.term, // search term
                        page: params.page || 1
                    }, extraParams);
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
                // cache: true
            },
            placeholder: placeholderText,
            minimumInputLength: minimumInputLength,
        }
    }
}