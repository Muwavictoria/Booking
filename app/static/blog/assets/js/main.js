// ==============================left sidebar js================================
$(document).on('click', '#sidebar li', function(){
    $(this).addClass('active').siblings().removeClass('active')
});


// ==================================left menu sid bardp toggle=================================

$(".sub-menu ul").hide();
$(".sub-menu a").click(function() {
    $(this).parent(".sub-menu").children("ul").slideToggle("100");
    $(this).find(".right").toggleClass("fa-caret-up fa-caret-down");
});




// ===============side bar Tooggle=================================
$(document).ready(function(){
    $("#toggleSidebar").click(function(){
        $(".left-menu").toggleClass("hide");
        $(".content-wrapper").toggleClass("hide");
    });
});



// searchbar box and icon 
let search = document.querySelector('.search-box');


document.querySelector('#search-icon').onclick = () =>{
    search.classList.toggle('active');
}

// ============================options links cars========================================
document.addEventListener('DOMContentLoaded', function () {
    var toggleIcon = document.getElementById('toggle-icon');
    var optionsCheck = document.getElementById('options-check');

    toggleIcon.addEventListener('click', function () {
        // Toggle the visibility of the options-check
        if (optionsCheck.style.display === 'none' || optionsCheck.style.display === '') {
            optionsCheck.style.display = 'block';
        } else {
            optionsCheck.style.display = 'none';
        }

        // Toggle the plus/minus icon
        var iconClass = optionsCheck.style.display === 'none' ? 'fas fa-plus' : 'fas fa-minus';
        toggleIcon.className = iconClass;
    });
});

