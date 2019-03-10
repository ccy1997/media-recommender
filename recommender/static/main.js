favorites = [];

function search() {
    clearSearchResults();
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
                    clearSearchResults();

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
    var favorites_str = favorites.toString();

    var request = new XMLHttpRequest();
        request.open('GET', '/submit?favorites=' + favorites_str);

        request.onload = function() {
            console.log('test');
            var responseText = request.responseText;
            var recommendation = JSON.parse(responseText).recommendation;

            // For each recommendation title render a list item
            for (i = 0; i < recommendation.length; i++) {
                var title = recommendation[i].split('::')[0];
                var type = recommendation[i].split('::')[1];
                var li = document.createElement('li');
                li.classList.add('list-group-item');
                li.id = recommendation[i];
                li.textContent = title + ' (' + type + ')';
                document.getElementById('recommendation').appendChild(li);
            }
        }

        request.send();
}

// Remove all buttons within search_results <div>
function clearSearchResults() {
    var search_results = document.getElementById('search_results');
    while (search_results.firstChild) {
        search_results.removeChild(search_results.firstChild);
    }
}

function resetFavoritesAndRecommendation() {
    resetFavorites();
    resetRecommendationDisplay();
}

function resetFavorites() {
    favorites = [];
    console.log(favorites);
    resetFavoritesDisplay();
}

function update_favorites_display() {
    resetFavoritesDisplay();

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

// Remove all list item within favorites <div>
function resetFavoritesDisplay() {
    var favorites = document.getElementById("favorites");
    while (favorites.firstChild) {
        favorites.removeChild(favorites.firstChild);
    }
}

// Remove all list item within recommendation <div>
function resetRecommendationDisplay() {
    var recommendation = document.getElementById("recommendation");
    while (recommendation.firstChild) {
        recommendation.removeChild(recommendation.firstChild);
    }
}

function arrayContains(arr, el) {
    return (arr.indexOf(el) > -1);
}