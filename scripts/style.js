$(document).ready(function () {
  window.onclick = function (event) {
    if (!event.target.matches('.filter-dropdown-button')) {
      var dropdowns = document.getElementsByClassName("filter-dropdown-content");
      for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show-dropdown')) {
          openDropdown.classList.remove('show-dropdown');
        }
      }
    }
  }

})