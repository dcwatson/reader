var spinner = new Spinner();

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
    /*
    var num_read = $('ul.stories li.read').length;
    var num_unread = $('ul.stories li').length - num_read;
    $('#unread-' + feed_id).text(num_unread);
    */
}

STORY_CLASS_ACTIONS = {
    'starred': 'unstar',
    'unstarred': 'star',
    'read': 'unread',
    'unread': 'read'
};

$(function() {
    load_column('#feeds', '/feeds/');

    $('body').on('click', 'a.ajax', function(e) {
        $('li.selected', $(this).parent().parent()).removeClass('selected');
        $(this).parent().addClass('selected');
        load_column($(this).data('target'), $(this).attr('href'));
        return false;
    });

    $('body').on('click', 'a.add-feed', function(e) {
        $('#fade').show();
        $('#dialog').show();
        $('input.add-feed').focus().select();
        return false;
    });

    $('body').on('click', 'a.story-action', function(e) {
        var a = $(this);
        var action = '';
        $.each(STORY_CLASS_ACTIONS, function(key, value) {
            if(a.hasClass(key)) {
                action = value;
                return false;
            }
        });
        $.ajax({
            url: a.attr('href'),
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({action: action}),
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function(data) {
                if(action == 'star') {
                    a.removeClass('unstarred').addClass('starred');
                }
                else if(action == 'unstar') {
                    a.removeClass('starred').addClass('unstarred');
                }
                else if(action == 'read') {
                    a.removeClass('unread').addClass('read');
                    $('li[data-story="' + data.story + '"]').addClass('read');
                }
                else if(action == 'unread') {
                    a.removeClass('read').addClass('unread');
                    $('li[data-story="' + data.story + '"]').removeClass('read');
                }
            }
        })
        return false;
    });

    $('body').on('click', 'a.all-read', function(e) {
        var a = $(this);
        $.ajax({
            url: $(this).attr('href'),
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({action: 'read'}),
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function(data) {
                console.log(data);
                $('.stories li', a.parent().parent().parent()).addClass('read');
            }
        })
        return false;
    });
});
