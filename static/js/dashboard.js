


const navItems = document.querySelectorAll('.side-nav__item');
const removeClasses = () => {
    navItems.forEach(eachItem => {
        eachItem.classList.remove('side-nav__item-active');
    });
}

navItems.forEach(eachItem => {
    eachItem.addEventListener('click', function () {
        removeClasses();
        eachItem.classList.add('side-nav__item-active');
    });
});

$(document).ready(function () {
    var zindex = 10;

    $("div.card").click(function (e) {

        var isShowing = false;

        if ($(this).hasClass("show")) {
            isShowing = true
        }

        if ($("div.cards").hasClass("showing")) {
            // a card is already in view
            $("div.card.show")
                .removeClass("show");

            if (isShowing) {
                // this card was showing - reset the grid
                $("div.cards")
                    .removeClass("showing");
                    e.currentTarget.submit();
            } else {
                // this card isn't showing - get in with it
                $(this)
                    .css({zIndex: zindex})
                    .addClass("show");

            }

            zindex++;

        } else {
            // no cards in view
            $("div.cards")
                .addClass("showing");
            $(this)
                .css({zIndex: zindex})
                .addClass("show");

            zindex++;
        }

    });
});
