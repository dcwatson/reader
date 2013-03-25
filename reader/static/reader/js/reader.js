var spinner = new Spinner();

function load_column(col_sel, url) {
    var c = $(col_sel).empty();
    spinner.spin(c[0]);
    $.ajax({
        url: url,
        success: function(html) {
            spinner.stop();
            c.append(html);
        }
    });
}

function update_unread_count(feed_id) {
    var num_read = $('ul.stories li.read').length;
    var num_unread = $('ul.stories li').length - num_read;
    console.log(feed_id, num_read, num_unread);
    $('#unread-' + feed_id).text(num_unread);
}

$(function() {
    load_column('#feeds', '/feeds/');
    
    $('body').on('click', 'a.ajax', function(e) {
        load_column($(this).data('target'), $(this).attr('href'));
        return false;
    });
    
    $('body').on('click', 'a.add-feed', function(e) {
        $('#fade').show();
        $('#dialog').show();
        $('input.add-feed').focus().select();
        return false;
    });
});
