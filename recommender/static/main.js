favorites = [];

function search() {
    removeAllChild('search_results');
    var query = document.getElementById("search").value.trim();

    // Process and send the query if it does not just consist of whitespaces
    if (query) {
        var request = new XMLHttpRequest();
        request.open('GET', '/search?query=' + query);

        request.onload = function() {
            var responseText = request.responseText;
            var search_results = JSON.parse(responseText).results;

            // For each searched title render a button within the search_result <div>
            for (i = 0; i < search_results.length; i++) {
                var title = search_results[i].split('::')[0];
                var type = search_results[i].split('::')[1];
                var button = document.createElement('button');
                button.classList.add('list-group-item');
                button.classList.add('list-group-item-action');
                button.id = search_results[i];
                button.textContent = title + ' (' + type + ')';  
                document.getElementById('search_results').appendChild(button);

                // On mouse down listener for the button
                button.onmousedown = function() {
                    removeAllChild('search_results')

                    // Clear the search bar
                    document.getElementById('search').value = '';

                    // Update the favorites array and list display
                    if (!arrayContains(favorites, this.id)) {
                        favorites.push(this.id);
                        console.log(favorites);
                        update_favorites_display();
                    }

                };
            }
        }

        request.send();
    }
}

function submit_favorites() {
    if (favorites.length != 0) {
        document.getElementById('alert_row').style.display = 'none';
        var favorites_str = encodeURIComponent(favorites.toString());

        var request = new XMLHttpRequest();
            request.open('GET', '/submit?favorites=' + favorites_str);
    
            request.onload = function() {
                removeAllChild('movie_recommendation');
                removeAllChild('game_recommendation');
                removeAllChild('book_recommendation');
                
                var jsonResponse = JSON.parse(request.responseText);
                var movie_recommendation = jsonResponse.movie;
                var game_recommendation = jsonResponse.game;
                var book_recommendation = jsonResponse.book;
    
                // For each movie recommendation title render a list item
                for (i = 0; i < movie_recommendation.length; i++) {
                    var title = movie_recommendation[i];
                    var li = document.createElement('li');
                    li.classList.add('list-group-item');
                    li.id = title;
                    li.textContent = title;
                    document.getElementById('movie_recommendation').appendChild(li);
                }
    
                // For each game recommendation title render a list item
                for (i = 0; i < game_recommendation.length; i++) {
                    var title = game_recommendation[i];
                    var li = document.createElement('li');
                    li.classList.add('list-group-item');
                    li.id = title;
                    li.textContent = title;
                    document.getElementById('game_recommendation').appendChild(li);
                }
    
                // For each book recommendation title render a list item
                for (i = 0; i < book_recommendation.length; i++) {
                    var title = book_recommendation[i];
                    var li = document.createElement('li');
                    li.classList.add('list-group-item');
                    li.id = title;
                    li.textContent = title;
                    document.getElementById('book_recommendation').appendChild(li);
                }
    
            }
    
            request.send();
    }
    else {
        document.getElementById('alert_row').style.display = 'block';
    }
}

function reset() {
    removeFavorites();
    removeAllChild('movie_recommendation');
    removeAllChild('game_recommendation');
    removeAllChild('book_recommendation');
    document.getElementById('alert_row').style.display = 'none';
}

function removeFavorites() {
    favorites = [];
    console.log(favorites);
    removeAllChild('favorites');
}

function update_favorites_display() {
    removeAllChild('favorites');

    for (i = 0; i < favorites.length; i++) {
        // Create a list item for the favorite item
        var title = favorites[i].split('::')[0];
        var type = favorites[i].split('::')[1];
        var li = document.createElement('li');
        li.classList.add('list-group-item');
        li.id = favorites[i];
        li.textContent = title + ' (' + type + ')';
        document.getElementById('favorites').appendChild(li);

        // Create a delete button for the favorite item
        var delete_button = document.createElement('button');
        delete_button.id = favorites[i];
        delete_button.type = 'button';
        delete_button.classList.add('close');
        delete_button.classList.add('float-right');
        delete_button.innerHTML = '&times;';
        li.appendChild(delete_button);

        // On mouse down listener for the delete button
        delete_button.onmousedown = function() {
            var favoriteToBeRemovedIndex = favorites.indexOf(this.id);
            favorites.splice(favoriteToBeRemovedIndex, 1);
            var liToBeRemoved = document.getElementById(this.id);
            liToBeRemoved.parentNode.removeChild(liToBeRemoved);
        };
    }
}

function removeAllChild(id) {
    var element = document.getElementById(id);
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function arrayContains(arr, el) {
    return (arr.indexOf(el) > -1);
}