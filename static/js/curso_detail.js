document.getElementById('add-material-btn').addEventListener('click', function() {
    var form = document.getElementById('add-material-form');
    if (form.style.display === 'none') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
});