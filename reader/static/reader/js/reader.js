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

function update_document_title() {
    var total = 0;
    $('span.unread').each(function(idx, elem) {
        try {
            total += parseInt($(elem).text());
        }
        catch(e) {
        }
    });
    var title = 'Reader';
    if(total > 0)
        title += ' (' + total + ')';
    $(document).attr('title', title);
}

function load_column(col_sel, url) {
    var c = $(col_sel).empty();
    spinner.spin(c[0]);
    $.ajax({
        url: url,
        success: function(html) {
            $('#story').empty();
            spinner.stop();
            c.append(html);
            if(col_sel == '#feeds')
                update_document_title();
        }
    });
}

function update_unread_count(feed_id, zero) {
    try {
        var e = $('a.feed[data-feed="' + feed_id + '"] > span.unread');
        var num = parseInt(e.text());
        var by = zero ? num : 1;
        var new_num = Math.max(num - by, 0);
        e.text(new_num);
        if(new_num == 0) {
            e.parent().parent().removeClass('unread');
        }
    }
    catch(e) {
    }
    update_document_title();
}

STORY_CLASS_ACTIONS = {
    'starred': 'unstar',
    'unstarred': 'star',
    'read': 'unread',
    'unread': 'read'
};

function reader_reset() {
    $('#stories').empty();
    $('#story').empty();
    load_column('#feeds', '/feeds/');
}

$(function() {
    $('.autoload').each(function(idx, elem) {
        var url = $(elem).data('autoload-url');
        load_column(elem, url);
    });

    $('body').on('update-unread', function(e, feed_id) {
        update_unread_count(feed_id);
    });

    $('body').on('click', 'a.ajax', function(e) {
        $('li.selected', $(this).parent().parent()).removeClass('selected');
        $(this).parent().addClass('selected');
        load_column($(this).data('target'), $(this).attr('href'));
        return false;
    });

    $('body').on('click', 'div.story a', function(e) {
        $(this).attr('target', '_blank');
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
                $('.stories li', a.parent().parent().parent()).addClass('read');
                if(a.data('feed')) {
                    update_unread_count(a.data('feed'), true);
                }
                else {
                    $('span.unread').text(0);
                }
            }
        })
        return false;
    });

    $('body').on('click', 'button.unsubscribe', function(e) {
        var name = $(this).data('name');
        return confirm('Are you sure you want to unsubscribe from "' + name + '"?');
    });

    $('body').on('submit', '#search-form', function(e) {
        var url = $(this).attr('action') + '?' + $(this).serialize();
        load_column('#stories', url);
        return false;
    });
});
