import { ArticleJsFunctions, CommonJsFunctions } from '../globalFunctions.js';

$(document).ready(function () {
    // const articleFunctions = new ArticleAddJsFunctions();
    const globalFunctions = new CommonJsFunctions();

    $(document).on('click', '#btnSaveArticle', function () {
        let apiURL = '/api/v1/article/save';
        let method = 'POST';
        let data = JSON.stringify({
            title: $(this).data('title'),
            url: $(this).data('url'),
            description: $(this).data('description'),
            article_image_url: $(this).data('article_image_url'),
            sentiment: $(this).data('sentiment'),
            published_at: $(this).data('published_at'),
        });
        let dataType = 'json';
        let processingButton = this;
        let postProcessing = (responseData) => {
            window.location.href = '/saved-articles';
        }
        let showSuccessMessage = true;
        globalFunctions.performPostAPICall(apiURL, method, data, dataType,
            processingButton, postProcessing, showSuccessMessage);
    });
});
