
function Dragen() {
    this.tr = $(".table-tr");
    this.tbody = $(".tbodyOfTable")
}

Dragen.prototype.onhoverEvent = function(){
    var self = this;
    self.tr.hover(function(){
        $(this).removeClass("bg-warning")
    },function(){
        $(this).addClass("bg-warning")
    })
};

Dragen.prototype.Run = function() {
    this.onhoverEvent();
};
$(function(){
    var gragen = new Dragen();
    gragen.Run();
});