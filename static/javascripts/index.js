$("#recentButton").click(function() {
    $("#featuredButton").removeClass("active");
    $("#recent").show();
    $("#recentButton").addClass("active");
    $("#featured").hide();
});

function indexSetup() {
    $("#featuredButton").addClass("active");
    $("#recent").hide();
    $("#recentButton").removeClass("active");
    $("#featured").show();
}

$("#featuredButton").click(function() {
    indexSetup();
})

$(document).ready(function () {
    indexSetup();
});
