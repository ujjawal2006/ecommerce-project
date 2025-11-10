function toggleDropdown() {
    var dropdown = document.getElementById("accountDropdown");
    dropdown.classList.toggle("open");
  }
  
  // Close dropdown if clicked outside
  window.onclick = function(event) {
    if (!event.target.matches('#accountDropdown > a')) {
      var dropdowns = document.getElementsByClassName("dropdown");
      for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        openDropdown.classList.remove('open');
      }
    }
  }
 