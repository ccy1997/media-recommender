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

            // For each searched title render a <button> element
            for (i = 0; i < search_results.length; i++) {
                var title = search_results[i].split('::')[0];
                var type = search_results[i].split('::')[1];
                var button = document.createElement('button');
                button.classList.add('list-group-item');
                button.classList.add('list-group-item-action');
                button.value = search_results[i];
                button.textContent = title + ' (' + type + ')';
                button.onmousedown = function() {
                    clearSearchResults();
                    document.getElementById('search').value = '';

                    if (!arrayContains(favorites, this.value)) {
                        favorites.push(this.value);
                        console.log(favorites);
                        update_favorites_display();
                    }

                };
                document.getElementById('search_results').appendChild(button);
            }
        }

        request.send();
    }
}

// Remove all buttons within search_results <div>
function clearSearchResults() {
    var search_results = document.getElementById("search_results");
    while (search_results.firstChild) {
        search_results.removeChild(search_results.firstChild);
    }
}

function update_favorites_display() {
    resetFavoritesDisplay();

    for (i = 0; i < favorites.length; i++) {
        var title = favorites[i].split('::')[0];
        var type = favorites[i].split('::')[1];
        var button = document.createElement('button');
        button.classList.add('list-group-item');
        button.classList.add('list-group-item-action');
        button.value = title;
        button.textContent = title + ' (' + type + ')';
        button.draggable = true;
        document.getElementById('favorites').appendChild(button);
    }
}

function resetFavorites() {
    favorites = [];
    console.log(favorites);
    resetFavoritesDisplay();
}

// Remove all buttons within favorites <div>
function resetFavoritesDisplay() {
    var favorites = document.getElementById("favorites");
    while (favorites.firstChild) {
        favorites.removeChild(favorites.firstChild);
    }
}

function arrayContains(arr, el) {
    return (arr.indexOf(el) > -1);
}