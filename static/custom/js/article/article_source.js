import { ArticleJsFunctions, CommonJsFunctions } from '../globalFunctions.js';

$(document).ready(function () {
    // const articleFunctions = new ArticleAddJsFunctions();
    //    const globalFunctions = new CommonJsFunctions();

    $('#sources').select2({
        ajax: {
            url: '/api/v1/article_api/get_sources',
            data: function (params) {
                var query = {
                    // search: params.term,
                    page: params.page || 1
                }

                // Query parameters will be ?search=[term]&page=[page]
                return query;
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
            }
        }
    });
});
