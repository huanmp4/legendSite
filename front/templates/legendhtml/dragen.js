
function Dragen() {
    this.tr = $(".table-tr");
    this.tbody = $(".tbodyOfTable");
    this.inputsi = $(".input-si");
    this.btnSubmit = $("#btn-search-submit");
    this.formtable = $("#formTable");
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
    });

    //
    self.inputsi.css("background","rgba(0,0,0,0.3)")
};

Dragen.prototype.onSubmitSearch = function(){
    var self = this;
    self.btnSubmit.click(function(event){
        event.preventDefault();
        console.log("event:",event);
        console.log("btnSubmit:",self.btnSubmit);
        var content = self.formtable.find("input[name='content']").val()
        console.log("content:",content)
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
    this.onSubmitSearch();
};




$(function(){
    var gragen = new Dragen();
    gragen.Run();
    gragen.firstLoad();
});