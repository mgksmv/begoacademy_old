$(function () {
    let current = location.pathname;
    $('#category-nav .category-item').each(function () {
        let $this = $(this);
        // if the current path is like this link, make it active
        if ($this.attr('href').indexOf(current) !== -1) {
            $this.addClass('active');
        }
    })
})