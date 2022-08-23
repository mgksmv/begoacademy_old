$(document).ready(function () {
    $('#more-btn').on('click', function () {
        let moreBtn = document.getElementById('more-btn');
        let moreDiv = document.getElementById('more-div');

        if (moreDiv.style.display === 'none') {
            moreDiv.style.display = 'block';
            moreBtn.innerHTML = '<i class="fas fa-arrow-up"></i>  Скрыть категории'
        } else {
            moreDiv.style.display = 'none';
            moreBtn.innerHTML = '<i class="fas fa-align-justify"></i>  Категории семинаров'
        }
    })
})
