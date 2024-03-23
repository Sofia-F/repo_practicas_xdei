document.addEventListener('DOMContentLoaded', function() {
    var navLinks = document.querySelectorAll('.navbar a');

    navLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default link behavior

            // Remove 'active' class from all links
            navLinks.forEach(function(link) {
                link.classList.remove('active');
            });

            // Add 'active' class to the clicked link
            this.classList.add('active');
        });
    });
});
