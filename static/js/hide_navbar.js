let prevScrollPos = window.scrollY;
window.isMobile = /iphone|ipod|ipad|android|blackberry|opera mini|opera mobi|skyfire|maemo|windows phone|palm|iemobile|symbian|symbianos|fennec/i.test(navigator.userAgent.toLowerCase());
if (window.isMobile) {
    window.onscroll = function () {
    let currentScrollPos = window.scrollY;
        if (prevScrollPos > currentScrollPos) {
            document.getElementById('navbar').style.top = '0';
        } else {
            document.getElementById('navbar').style.top = '-100px';
        }
        prevScrollPos = currentScrollPos;
    }
}
