import { ArticleJsFunctions, CommonJsFunctions } from '../globalFunctions.js';

$(document).ready(function () {
    // const articleFunctions = new ArticleAddJsFunctions();
    const globalFunctions = new CommonJsFunctions();

    $('#sources').select2(globalFunctions.fetchSelect2Data(
        '/api/v1/article_api/get_sources',
        'Search for a news source', 0));

    $('#country').select2(globalFunctions.fetchSelect2Data(
        '/api/v1/article_api/get_get_country_lang_category?resource_type=country',
        'Search for a country', 0));

    $('#language').select2(globalFunctions.fetchSelect2Data(
        '/api/v1/article_api/get_get_country_lang_category?resource_type=language',
        'Search for a news language', 0));

    $('#category').select2(globalFunctions.fetchSelect2Data(
        '/api/v1/article_api/get_get_country_lang_category?resource_type=category',
        'Search for a news category', 0));

});
