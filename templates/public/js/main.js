function delay(callback, ms) {
  var timer = 0;

  return function() {
    clearTimeout(timer);
    timer = setTimeout(callback, ms);
  };
};

function sort(container, sortAscendingIcon, sortDescendingIcon) {
  container.classList.toggle('flex-col-reverse');

  sortAscendingIcon.classList.toggle('hidden');
  sortDescendingIcon.classList.toggle('hidden');
}

function search(inputValue) {
  const filter = inputValue.trim().toLowerCase();
  let found = false;

  const searchingMessage = document.getElementById('searching')
  searchingMessage.classList.remove('hidden');

  for (let i = 0; i < packages.length; i++) {
    let package = packages[i];
    let name = package.name.toLowerCase();
    let summary = package.summary.toLowerCase();
    let keywords = package.keywords || [];

    if (name.indexOf(filter) > -1 || summary.indexOf(filter) > -1 || keywords.indexOf(filter) > -1) {
      found = true;
      let element = document.getElementById(package.name);
      element.classList.remove('hidden');
    } else {
      let element = document.getElementById(package.name);
      element.classList.add('hidden');
    }
  }

  let noResultsMessage = document.getElementById('no-results');
  if (found) {
    noResultsMessage.classList.add('hidden');
  } else {
    noResultsMessage.classList.remove('hidden');
  }

  searchingMessage.classList.add('hidden');
}

window.addEventListener("load", function() {
  const searchInput = document.getElementById('search-input');
  const packagesContainer = document.getElementById('packages');

  const sortButton = document.getElementById('sort-button');
  const sortAscendingIcon = document.getElementById('sort-ascending');
  const sortDescendingIcon = document.getElementById('sort-descending');

  search(searchInput.value);

  searchInput.addEventListener('input', delay(function() {
    search(searchInput.value);
  }, 100));

  sortButton.addEventListener('click', function() {
    sort(packagesContainer, sortAscendingIcon, sortDescendingIcon);
  });
});
