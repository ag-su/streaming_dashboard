window.onscroll = function() {
    let navbar = document.getElementById("navbar");
    let navbar_title = document.getElementById("navbar-title");
    let link_class_1 = document.getElementById("link-class-1");
    let link_class_2 = document.getElementById("link-class-2");

    if (window.scrollY > 70) {
        navbar.classList.add("shrink");
        navbar_title.classList.add("shrink");
        link_class_1.classList.add("shrink");
        link_class_2.classList.add("shrink");


    } else {
        navbar.classList.remove("shrink");
        navbar_title.classList.remove("shrink");
        link_class_1.classList.remove("shrink");
        link_class_2.classList.remove("shrink");
    }
};