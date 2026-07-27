/*====================================================
   SKIN AI
   COMPLETE SCRIPT.JS
   Image Upload + UI + Navigation + Theme + Loader
====================================================*/


/*====================================================
   DOM READY
====================================================*/

document.addEventListener("DOMContentLoaded", function () {


    /*================================================
       ELEMENTS
    =================================================*/

    const imageInput =
        document.getElementById("imageInput");

    const previewContainer =
        document.getElementById("previewContainer");

    const previewImage =
        document.getElementById("previewImage");

    const dropZone =
        document.getElementById("dropZone");

    const navbar =
        document.querySelector(".navbar");

    const scrollBtn =
        document.getElementById("scrollTop");

    const themeBtn =
        document.getElementById("themeToggle");

    const menuBtn =
        document.querySelector(".menu-toggle");

    const navLinks =
        document.querySelector(".nav-links");

    const loader =
        document.querySelector(".loading-screen");


    /*================================================
       IMAGE PREVIEW
    =================================================*/

    function previewFile(file) {

        if (!file) {
            return;
        }


        /* Validate image */

        if (!file.type.startsWith("image/")) {

            alert(
                "Please select a valid image file."
            );

            if (imageInput) {
                imageInput.value = "";
            }

            return;
        }


        /* Validate file size
           Maximum = 10 MB */

        const maxSize =
            10 * 1024 * 1024;


        if (file.size > maxSize) {

            alert(
                "Image size should be less than 10 MB."
            );

            if (imageInput) {
                imageInput.value = "";
            }

            return;
        }


        /* File reader */

        const reader =
            new FileReader();


        reader.onload =
            function (event) {

                if (previewContainer) {

                    previewContainer.style.display =
                        "block";

                }


                if (previewImage) {

                    previewImage.src =
                        event.target.result;

                }

            };


        reader.onerror =
            function () {

                alert(
                    "Unable to preview this image."
                );

            };


        reader.readAsDataURL(file);

    }


    /*================================================
       FILE INPUT CHANGE
    =================================================*/

    if (imageInput) {

        imageInput.addEventListener(
            "change",
            function () {

                const file =
                    this.files[0];

                previewFile(file);

            }
        );

    }


    /*================================================
       DRAG OVER
    =================================================*/

    if (dropZone) {

        dropZone.addEventListener(
            "dragover",
            function (event) {

                event.preventDefault();

                dropZone.style.borderColor =
                    "#2563eb";

                dropZone.style.background =
                    "#eef6ff";

                dropZone.style.transform =
                    "translateY(-3px)";

            }
        );


        /*============================================
           DRAG LEAVE
        ============================================*/

        dropZone.addEventListener(
            "dragleave",
            function () {

                dropZone.style.borderColor =
                    "#93c5fd";

                dropZone.style.background =
                    "#f8fbff";

                dropZone.style.transform =
                    "translateY(0)";

            }
        );


        /*============================================
           DROP
        ============================================*/

        dropZone.addEventListener(
            "drop",
            function (event) {

                event.preventDefault();


                dropZone.style.borderColor =
                    "#93c5fd";

                dropZone.style.background =
                    "#f8fbff";

                dropZone.style.transform =
                    "translateY(0)";


                const files =
                    event.dataTransfer.files;


                const file =
                    files[0];


                if (!file) {
                    return;
                }


                if (
                    imageInput &&
                    file.type.startsWith("image/")
                ) {

                    try {

                        /*
                         * Put dropped file
                         * into file input
                         */

                        const dataTransfer =
                            new DataTransfer();

                        dataTransfer.items.add(file);

                        imageInput.files =
                            dataTransfer.files;

                    }
                    catch (error) {

                        console.warn(
                            "Could not assign dropped file.",
                            error
                        );

                    }


                    previewFile(file);

                }
                else {

                    alert(
                        "Please drop a valid image file."
                    );

                }

            }
        );

    }


    /*================================================
       COUNTER ANIMATION
    =================================================*/

    const counters =
        document.querySelectorAll(".counter");


    function startCounter(counter) {

        if (
            counter.dataset.started === "true"
        ) {
            return;
        }


        counter.dataset.started =
            "true";


        const target =
            parseInt(
                counter.getAttribute(
                    "data-target"
                )
            ) || 0;


        let count = 0;


        const duration = 1200;

        const startTime =
            performance.now();


        function updateCounter(currentTime) {

            const elapsed =
                currentTime - startTime;


            const progress =
                Math.min(
                    elapsed / duration,
                    1
                );


            /*
             * Smooth easing
             */

            const eased =
                1 -
                Math.pow(
                    1 - progress,
                    3
                );


            count =
                Math.floor(
                    eased * target
                );


            counter.innerText =
                count;


            if (progress < 1) {

                requestAnimationFrame(
                    updateCounter
                );

            }
            else {

                counter.innerText =
                    target;

            }

        }


        requestAnimationFrame(
            updateCounter
        );

    }


    /*================================================
       COUNTER OBSERVER
    =================================================*/

    if (
        counters.length > 0 &&
        "IntersectionObserver" in window
    ) {

        const counterObserver =
            new IntersectionObserver(
                function (entries) {

                    entries.forEach(
                        function (entry) {

                            if (
                                entry.isIntersecting
                            ) {

                                startCounter(
                                    entry.target
                                );

                                counterObserver.unobserve(
                                    entry.target
                                );

                            }

                        }
                    );

                },
                {
                    threshold: 0.5
                }
            );


        counters.forEach(
            function (counter) {

                counterObserver.observe(
                    counter
                );

            }
        );

    }
    else {

        counters.forEach(
            function (counter) {

                startCounter(counter);

            }
        );

    }


    /*================================================
       STICKY NAVBAR
    =================================================*/

    function updateNavbar() {

        if (!navbar) {
            return;
        }


        if (window.scrollY > 80) {

            navbar.style.top =
                "0px";

            navbar.style.borderRadius =
                "0 0 18px 18px";

            navbar.style.width =
                "100%";

            navbar.style.background =
                "rgba(255,255,255,.96)";

            navbar.style.boxShadow =
                "0 10px 30px rgba(0,0,0,.10)";

        }
        else {

            navbar.style.top =
                "20px";

            navbar.style.width =
                "92%";

            navbar.style.borderRadius =
                "20px";

            navbar.style.background =
                "rgba(255,255,255,.90)";

            navbar.style.boxShadow =
                "0 10px 35px rgba(0,0,0,.08)";

        }

    }


    window.addEventListener(
        "scroll",
        updateNavbar
    );


    updateNavbar();


    /*================================================
       SCROLL TO TOP
    =================================================*/

    if (scrollBtn) {

        scrollBtn.style.display =
            "none";


        function updateScrollButton() {

            if (
                window.scrollY > 400
            ) {

                scrollBtn.style.display =
                    "flex";

            }
            else {

                scrollBtn.style.display =
                    "none";

            }

        }


        window.addEventListener(
            "scroll",
            updateScrollButton
        );


        scrollBtn.addEventListener(
            "click",
            function () {

                window.scrollTo({

                    top: 0,

                    behavior: "smooth"

                });

            }
        );

    }


    /*================================================
       LOADING SCREEN
    =================================================*/

    window.addEventListener(
        "load",
        function () {

            if (!loader) {
                return;
            }


            loader.style.opacity =
                "0";


            loader.style.pointerEvents =
                "none";


            setTimeout(
                function () {

                    loader.style.display =
                        "none";

                },
                600
            );

        }
    );


    /*================================================
       DARK MODE
    =================================================*/

    if (themeBtn) {

        const themeIcon =
            themeBtn.querySelector("i");


        /*
         * Restore saved theme
         */

        const savedTheme =
            localStorage.getItem(
                "theme"
            );


        if (
            savedTheme === "dark"
        ) {

            document.body.classList.add(
                "dark"
            );


            if (themeIcon) {

                themeIcon.classList.remove(
                    "fa-moon"
                );

                themeIcon.classList.add(
                    "fa-sun"
                );

            }

        }


        /*============================================
           THEME BUTTON
        ============================================*/

        themeBtn.addEventListener(
            "click",
            function () {

                document.body.classList.toggle(
                    "dark"
                );


                const isDark =
                    document.body.classList.contains(
                        "dark"
                    );


                if (themeIcon) {

                    if (isDark) {

                        themeIcon.classList.remove(
                            "fa-moon"
                        );

                        themeIcon.classList.add(
                            "fa-sun"
                        );

                    }
                    else {

                        themeIcon.classList.remove(
                            "fa-sun"
                        );

                        themeIcon.classList.add(
                            "fa-moon"
                        );

                    }

                }


                localStorage.setItem(
                    "theme",
                    isDark
                        ? "dark"
                        : "light"
                );

            }
        );

    }


    /*================================================
       MOBILE MENU
    =================================================*/

    if (
        menuBtn &&
        navLinks
    ) {

        menuBtn.addEventListener(
            "click",
            function () {

                navLinks.classList.toggle(
                    "show-menu"
                );


                /*
                 * Change hamburger icon
                 */

                const menuIcon =
                    menuBtn.querySelector("i");


                if (menuIcon) {

                    const isOpen =
                        navLinks.classList.contains(
                            "show-menu"
                        );


                    if (isOpen) {

                        menuIcon.classList.remove(
                            "fa-bars"
                        );

                        menuIcon.classList.add(
                            "fa-xmark"
                        );

                    }
                    else {

                        menuIcon.classList.remove(
                            "fa-xmark"
                        );

                        menuIcon.classList.add(
                            "fa-bars"
                        );

                    }

                }

            }
        );


        /*
         * Close mobile menu
         * when a link is clicked
         */

        navLinks
            .querySelectorAll("a")
            .forEach(
                function (link) {

                    link.addEventListener(
                        "click",
                        function () {

                            navLinks.classList.remove(
                                "show-menu"
                            );


                            const menuIcon =
                                menuBtn.querySelector(
                                    "i"
                                );


                            if (menuIcon) {

                                menuIcon.classList.remove(
                                    "fa-xmark"
                                );

                                menuIcon.classList.add(
                                    "fa-bars"
                                );

                            }

                        }
                    );

                }
            );

    }


    /*================================================
       ACTIVE NAV LINK
    =================================================*/

    const sections =
        document.querySelectorAll(
            "section[id]"
        );


    const links =
        document.querySelectorAll(
            ".nav-links a"
        );


    function updateActiveNav() {

        if (
            sections.length === 0 ||
            links.length === 0
        ) {
            return;
        }


        let current =
            "";


        sections.forEach(
            function (section) {

                const sectionTop =
                    section.offsetTop - 180;


                const sectionHeight =
                    section.offsetHeight;


                if (
                    window.scrollY >= sectionTop &&
                    window.scrollY <
                    sectionTop + sectionHeight
                ) {

                    current =
                        section.getAttribute(
                            "id"
                        );

                }

            }
        );


        links.forEach(
            function (link) {

                link.classList.remove(
                    "active"
                );


                const href =
                    link.getAttribute(
                        "href"
                    );


                if (
                    href === "#" + current
                ) {

                    link.classList.add(
                        "active"
                    );

                }

            }
        );

    }


    window.addEventListener(
        "scroll",
        updateActiveNav
    );


    updateActiveNav();


    /*================================================
       SMOOTH SCROLL
    =================================================*/

    document
        .querySelectorAll(
            'a[href^="#"]'
        )
        .forEach(
            function (anchor) {

                anchor.addEventListener(
                    "click",
                    function (event) {

                        const targetId =
                            this.getAttribute(
                                "href"
                            );


                        if (
                            !targetId ||
                            targetId === "#"
                        ) {
                            return;
                        }


                        const target =
                            document.querySelector(
                                targetId
                            );


                        if (target) {

                            event.preventDefault();


                            const navbarHeight =
                                navbar
                                    ? navbar.offsetHeight
                                    : 0;


                            const targetPosition =
                                target.offsetTop -
                                navbarHeight -
                                25;


                            window.scrollTo({

                                top:
                                    Math.max(
                                        0,
                                        targetPosition
                                    ),

                                behavior:
                                    "smooth"

                            });

                        }

                    }
                );

            }
        );


    /*================================================
       ANALYZE BUTTON / FORM LOADING
    =================================================*/

    const predictionForm =
        document.querySelector(
            "form"
        );


    if (predictionForm) {

        predictionForm.addEventListener(
            "submit",
            function () {

                /*
                 * Only activate loading
                 * if an image is selected.
                 */

                if (
                    imageInput &&
                    imageInput.files &&
                    imageInput.files.length > 0
                ) {

                    const analyzeButton =
                        predictionForm.querySelector(
                            ".predict-btn, button[type='submit'], input[type='submit']"
                        );


                    if (analyzeButton) {

                        /*
                         * Prevent double-click
                         */

                        analyzeButton.disabled =
                            true;


                        if (
                            analyzeButton.tagName ===
                            "BUTTON"
                        ) {

                            analyzeButton.innerHTML =
                                "🔄 Analyzing Image...";

                        }
                        else {

                            analyzeButton.value =
                                "Analyzing Image...";

                        }

                    }


                    /*
                     * Show loading screen
                     * if it exists.
                     */

                    if (loader) {

                        loader.style.display =
                            "flex";

                        loader.style.opacity =
                            "1";

                        loader.style.pointerEvents =
                            "auto";

                    }

                }

            }
        );

    }


    /*================================================
       IMAGE UPLOAD CLICK SUPPORT
    =================================================*/

    if (dropZone && imageInput) {

        dropZone.addEventListener(
            "click",
            function (event) {

                /*
                 * Do not reopen file picker
                 * when clicking directly on
                 * label/input elements.
                 */

                if (
                    event.target.tagName ===
                    "INPUT" ||
                    event.target.tagName ===
                    "LABEL" ||
                    event.target.closest(
                        "label"
                    )
                ) {
                    return;
                }


                imageInput.click();

            }
        );

    }


    /*================================================
       ESC KEY
       Close mobile menu
    =================================================*/

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape"
            ) {

                if (navLinks) {

                    navLinks.classList.remove(
                        "show-menu"
                    );

                }


                if (menuBtn) {

                    const menuIcon =
                        menuBtn.querySelector(
                            "i"
                        );


                    if (menuIcon) {

                        menuIcon.classList.remove(
                            "fa-xmark"
                        );

                        menuIcon.classList.add(
                            "fa-bars"
                        );

                    }

                }

            }

        }
    );


});


/*====================================================
   RESULT PAGE SAFETY
   Chatbot is intentionally NOT duplicated here.

   The chatbot JavaScript is already inside
   result.html and communicates with:

        POST /chat

   This avoids duplicate event listeners.
====================================================*/


/*====================================================
   GLOBAL UTILITY
   Optional function for showing loading manually
====================================================*/

function showLoading(message) {

    const loader =
        document.querySelector(
            ".loading-screen"
        );


    const loadingText =
        document.getElementById(
            "loadingText"
        );


    if (loader) {

        loader.style.display =
            "flex";

        loader.style.opacity =
            "1";

        loader.style.pointerEvents =
            "auto";

    }


    if (
        loadingText &&
        message
    ) {

        loadingText.innerText =
            message;

    }

}


/*====================================================
   HIDE LOADING
====================================================*/

function hideLoading() {

    const loader =
        document.querySelector(
            ".loading-screen"
        );


    if (!loader) {
        return;
    }


    loader.style.opacity =
        "0";


    loader.style.pointerEvents =
        "none";


    setTimeout(
        function () {

            loader.style.display =
                "none";

        },
        500
    );

}