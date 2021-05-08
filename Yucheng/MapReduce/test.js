function (doc){
    if (doc.tweet) {
        if (doc.tweet.entities && doc.tweet.entities.hashtags) {
            doc.tweet.entities.hashtags.forEach(function (hashtag) {
                if (hashtag.text) {
                    emit(hashtag.text.toLowerCase(), 1);
                }
            }
            );
        }   
    }
}