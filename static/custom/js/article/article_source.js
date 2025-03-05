import { ArticleJsFunctions, CommonJsFunctions } from '../globalFunctions.js';

$(document).ready(function () {
    // const articleFunctions = new ArticleAddJsFunctions();
    const globalFunctions = new CommonJsFunctions();

    var countrySelection = $('#country').select2(globalFunctions.fetchSelect2Data(
        '/api/v1/article_api/get_country_lang_category?resource_type=country',
        'Search for a country', 0, {}));

    countrySelection.on("change", function (e) { 
        console.log("chang")
        $('#sources').trigger('change'); 
    });

    var countrySelection = $('#language').select2(globalFunctions.fetchSelect2Data(
        '/api/v1/article_api/get_country_lang_category?resource_type=language',
        'Search for a news language', 0, {}));

    var countrySelection = $('#category').select2(globalFunctions.fetchSelect2Data(
        '/api/v1/article_api/get_country_lang_category?resource_type=category',
        'Search for a news category', 0, {}));

    var sourcesSelection = $('#sources').select2(globalFunctions.fetchSelect2Data(
        '/api/v1/article_api/get_sources',
        'Search for a news source', 0, {
            language: $("#language").val() || null,
            country: $("#country").val() || null,
            category: $("#category").val() || null
        }));

    $(document).on('click', '#btnGetArticle', function () {
        let apiURL = '/api/v1/article_api/get_articles';
        let method = 'POST';
        let data = JSON.stringify({
            sources: $("#sources").val(),
            news_query: $("#news_query").val(),
            language: $("#language").val(),
            country: $("#country").val(),
            category: $("#category").val(),
            page_size: $("#page_size").val(),
            page: $("#page").val(),
        });
        let dataType = 'json';
        let processingButton = this;
        let postProcessing = (responseData) => {
            // window.location.href = '/saved-articles';
        }
        let showSuccessMessage = true;
        globalFunctions.performPostAPICall(apiURL, method, data, dataType,
            processingButton, postProcessing, showSuccessMessage);
    });

});
