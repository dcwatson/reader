var FEED_CACHE = {};

function story_link(story) {
    return $('<a />').attr({
        href: story.reader_url
    }).data({
        'feed-id': story.feed,
        'story-id': story.id
    }).text(story.title).addClass('story');
}

function show_feed(feed_id) {
    data = FEED_CACHE[feed_id];
    $('#feed-title').text(data.title);
    $('#stories').empty();
    for(var i = 0; i < data.stories.length; i++) {
        var story = data.stories[i];
        $('#stories').append($('<li />').append(story_link(story)));
    }
}

function show_story(feed_id, story_id) {
    data = FEED_CACHE[feed_id];
    var story = null;
    for(var i = 0; i < data.stories.length; i++) {
        story = data.stories[i];
        if(story.id == story_id) {
            break;
        }
    }
    $('#content').html(story.content);
    $('#story-title').text(story.title).attr('href', story.link);
}

$(function() {
    $('body').on('click', 'a.feed', function(e) {
        var feed_id = parseInt($(this).data('feed-id'));
        if(FEED_CACHE[feed_id]) {
            show_feed(feed_id);
        }
        else {
            $.ajax({
                url: $(this).attr('href'),
                success: function(data) {
                    FEED_CACHE[data.id] = data;
                    show_feed(feed_id);
                }
            });
        }
        return false;
    });
    
    $('body').on('click', 'a.story', function(e) {
        var feed_id = parseInt($(this).data('feed-id'));
        var story_id = parseInt($(this).data('story-id'));
        show_story(feed_id, story_id);
        return false;
    });
});
