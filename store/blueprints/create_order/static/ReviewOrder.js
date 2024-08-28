$('.toggle-table-button').on('click', function() {
    $(this).closest('form').find('table').toggleClass('hidden');
    $(this).text($(this).text().includes('Hide') ? 'Show order information' : 'Hide order information');
});
