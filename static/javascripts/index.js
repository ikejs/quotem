$("#recentButton").click(function() {
    $("#popularButton").removeClass("active");
    $("#recentButton").addClass("active");
});

$("#popularButton").click(function() {
    $("#recentButton").removeClass("active");
    $("#featuredButton").addClass("active");
});

function indexSetup() {
    $("#popularButton").addClass("active");
    $("#recentButton").removeClass("active");
}
