function ajaxSeminars(btnClasses) {
    $(btnClasses).each(function (index, el) {
        $(el).on('click', function (event) {
            $(btnClasses).removeClass('active')
            $(this).addClass('active')
            const type = btnClasses.split(' ')[0]
            const seminars_content = $('#seminars-content')
            const mobile_categories = $('.mobile-categories')
            let pageURL = $(el).val()

            event.preventDefault()

            $.ajax({
                url: pageURL,
                type: 'GET',
                beforeSend: function () {
                    $('.ajax-loader').show()
                    if (type === '.categories') {
                        $('.categories button.list-group-item').each(function (index, el) {
                            $(el).prop('disabled', true)
                        })
                    }
                    seminars_content.hide()
                },
                success: function (response) {
                    seminars_content.empty()
                    seminars_content.show().html(response.data)
                    if (type === '.categories' && mobile_categories.css('display') === 'block') {
                        $('html').animate(
                            {
                                scrollTop: mobile_categories.offset().top
                            },
                            500
                        );
                    }
                    $('.ajax-loader').hide()
                    $('.categories button.list-group-item').each(function (index, el) {
                        $(el).prop('disabled', false)
                    })
                }
            })

            event.stopImmediatePropagation()
            return false
        })
    })
}

$(document).ready(function () {
    ajaxSeminars('.pagination button.page-link')
    ajaxSeminars('.categories button.list-group-item')
})

$(document).ajaxStop(function () {
    ajaxSeminars('.pagination button.page-link')
    ajaxSeminars('.categories button.list-group-item')
})