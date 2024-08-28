$('.toggle-table-button').on('click', function() {
    $(this).closest('form').find('table').toggleClass('hidden');
});
