document.addEventListener('DOMContentLoaded', function () {
    console.log('Static script loaded');
    if (window.__INIT__) {
        console.log('Initial data:', window.__INIT__);
    }
});
