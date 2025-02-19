import { ArticleJsFunctions, CommonJsFunctions } from '../globalFunctions.js';

$(document).ready(function () {
    // const articleFunctions = new ArticleJsFunctions();
    const globalFunctions = new CommonJsFunctions();

    $(document).on('click', '#btnDeleteArticle', function () {
        let apiURL = '/api/v1/article/delete';
        let method = 'POST';
        let data = JSON.stringify({
            saved_article_id: $(this).data('saved_article_id')
        });
        let dataType = 'json';
        let processingButton = this;
        let postProcessing = (responseData) => {
            window.location.href = '/saved-articles';
        }
        let showSuccessMessage = true;
        Swal.fire({
            title: "Do you want to delete this article?",
            showDenyButton: true,
            showCancelButton: false,
            confirmButtonText: "Delete",
            denyButtonText: `Don't Delete`
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                globalFunctions.performPostAPICall(apiURL, method, data, dataType,
                    processingButton, postProcessing, showSuccessMessage);
            } else if (result.isDenied) {
                Swal.fire("Your data is safe", "", "success");
            }
        });
    });
});
