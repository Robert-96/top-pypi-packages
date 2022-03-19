function sort(container, label, sortAscendingIcon, sortDescendingIcon) {
  container.classList.toggle('flex-col-reverse');

  sortAscendingIcon.classList.toggle('hidden');
  sortDescendingIcon.classList.toggle('hidden');

  if (label.textContent == "Sort Descending") {
    label.textContent = "Sort Ascending";
  } else {
    label.textContent = "Sort Descending";
  }
}

window.addEventListener("load", function() {
  const packagesContainer = document.getElementById('packages');

  const sortButton = document.getElementById('sort-button');
  const sortLabel = document.getElementById('sort-label');
  const sortAscendingIcon = document.getElementById('sort-ascending');
  const sortDescendingIcon = document.getElementById('sort-descending');

  sortButton.addEventListener('click', function() {
    sort(packagesContainer, sortLabel, sortAscendingIcon, sortDescendingIcon);
  });
});
