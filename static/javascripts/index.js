$("#recentButton").click(function() {
    $("#featuredButton").removeClass("active");
    $("#recentButton").addClass("active");
});

$("#featuredButton").click(function() {
    $("#recentButton").removeClass("active");
    $("#featuredButton").addClass("active");
});

function indexSetup() {
    $("#featuredButton").addClass("active");
    $("#recentButton").removeClass("active");
}
