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

            // For each searched title render a button within the search_result list-group
            renderListGroupButtonsFromSearchResults(search_results);
        }

        request.send();
    }
}

function submit_favorites() {
    if (favorites.length != 0) {
        // Remove all recommendation currently displayed
        removeAllChild('movie_recommendation');
        removeAllChild('game_recommendation');
        removeAllChild('book_recommendation');

        // Display a load spinner
        document.getElementById("recommendation_load_spinner").style.display = 'inline-flex';

        var favorites_str = encodeURIComponent(favorites.toString());
        var request = new XMLHttpRequest();
        request.open('GET', '/submit?favorites=' + favorites_str);
    
        request.onload = function() {
            // Remove the load spinner
            document.getElementById("recommendation_load_spinner").style.display = 'none';

            var jsonResponse = JSON.parse(request.responseText);
            var movie_recommendation = jsonResponse.movie;
            var game_recommendation = jsonResponse.game;
            var book_recommendation = jsonResponse.book;

            renderRecommendationFromArray(movie_recommendation, 'movie_recommendation');
            renderRecommendationFromArray(game_recommendation, 'game_recommendation');
            renderRecommendationFromArray(book_recommendation, 'book_recommendation');
        }
    
            request.send();
    }
}

function reset() {
    removeFavorites();
    removeAllChild('movie_recommendation');
    removeAllChild('game_recommendation');
    removeAllChild('book_recommendation');
}

function renderListGroupButtonsFromSearchResults(search_results) {
    for (i = 0; i < search_results.length; i++) {
        var title = search_results[i].split('::')[0];
        var type = search_results[i].split('::')[1];
        var button = document.createElement('button');
        button.id = search_results[i];
        button.classList.add('list-group-item');
        button.classList.add('list-group-item-action');
        button.textContent = title + ' (' + type + ')';  
        document.getElementById('search_results').appendChild(button);

        button.onmousedown = function() {
            removeAllChild('search_results')

            // Clear the search bar
            document.getElementById('search').value = '';

            // Update the favorites array and list-group display
            if (!arrayContains(favorites, this.id)) {
                favorites.push(this.id);
                console.log(favorites);
                renderFavorites();
            }

        };
    }
}

function renderFavorites() {
    // Remove all favorites currently displayed
    removeAllChild('movie_favorites');
    removeAllChild('game_favorites');
    removeAllChild('book_favorites');

    for (i = 0; i < favorites.length; i++) {
        // Create a list item for the favorite item
        var title = favorites[i].split('::')[0];
        var type = favorites[i].split('::')[1];
        var li = document.createElement('li');
        li.id = favorites[i];
        li.classList.add('list-group-item');
        li.classList.add('clearfix');
        li.textContent = title;
        li.style.borderRadius = '10px';

        // Render the list item in the appropriate list-group depends on item type
        if (type == 'Movie') {
            document.getElementById('movie_favorites').appendChild(li);
        }
        else if (type == 'Game') {
            document.getElementById('game_favorites').appendChild(li);
        }
        else if (type == 'Book') {
            document.getElementById('book_favorites').appendChild(li);
        }

        // Create and render a delete button for the list item
        var delete_button = createDeleteButton(favorites[i]);
        li.appendChild(delete_button);
    }
}

function renderRecommendationFromArray(arr, list_group_id) {
    for (i = 0; i < arr.length; i++) {
        var title = arr[i];
        var li = document.createElement('li');
        li.classList.add('list-group-item');
        li.classList.add('clearfix');
        li.id = title;
        li.textContent = title;
        li.style.borderRadius = '10px'
        document.getElementById(list_group_id).appendChild(li);
    }
}

function createDeleteButton(id) {
    var delete_button = document.createElement('button');
    delete_button.id = id;
    delete_button.type = 'button';
    delete_button.classList.add('close');
    delete_button.innerHTML = '&times;';

    delete_button.onmousedown = function() {
        var favoriteToBeRemovedIndex = favorites.indexOf(this.id);
        favorites.splice(favoriteToBeRemovedIndex, 1);
        var liToBeRemoved = document.getElementById(this.id);
        liToBeRemoved.parentNode.removeChild(liToBeRemoved);
    };

    return delete_button;
}

function removeFavorites() {
    favorites = [];
    removeAllChild('movie_favorites');
    removeAllChild('game_favorites');
    removeAllChild('book_favorites');
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