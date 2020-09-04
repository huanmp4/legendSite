
function Dragen() {
    this.tr = $(".table-tr");
    this.tbody = $(".tbodyOfTable")
}

Dragen.prototype.onhoverEvent = function(){
    var self = this;
    var oldclass = '';
    self.tr.hover(function(){
        oldclass = $(this).attr("class");
        console.log("oldclass",oldclass);
        $(this).removeClass(oldclass);
        $(this).removeClass(oldclass);
    },function(){
        $(this).addClass(oldclass)
    })
};

Dragen.prototype.firstLoad = function(){
    setTimeout(function () {
          $('.jumbotron').show();
        }, 500);
    $('item-4').css('background', 'rgba(255, 255, 255, .1)');
};

Dragen.prototype.Run = function() {
    this.onhoverEvent();
};




$(function(){
    var gragen = new Dragen();
    gragen.Run();
    gragen.firstLoad();
});