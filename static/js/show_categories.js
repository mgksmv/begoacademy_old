function showMore() {
    var moreBtn = document.getElementById("moreBtn");
    var moreDiv = document.getElementById("moreDiv");

    if (moreDiv.style.display === 'none') {
        moreDiv.style.display='block';
        moreBtn.innerHTML = '<i class="fas fa-arrow-up"></i>  Скрыть категории'
    } else {
        moreDiv.style.display = 'none';
        moreBtn.innerHTML = '<i class="fas fa-align-justify"></i>  Категории семинаров'
    }
}