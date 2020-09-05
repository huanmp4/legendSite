
function Dragen() {
    this.tr = $(".table-tr");
    this.tbody = $(".tbodyOfTable");
    this.inputsi = $(".input-si");
    this.btnSubmit = $(".btn-search-submit");
    this.formtable = $("#formTable");
    this.btn1 = $(".btn-search-submit1");
    this.btn2 = $(".btn-search-submit2");
    this.btn3 = $(".btn-search-submit3");
    this.btn4 = $(".btn-search-submit4");
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



Dragen.prototype.ax = function(e){
    console.log("e:",e);
    var self = this;
    $('.template-table-s').remove();
    // var old = $('.nameold').html();
    // var oneSevenSix = $('.name176').html();
    // var oneEightZero = $('.name180').html();
    // var singleOccupation = $('.namesingleOccupation').html();
    var finalContent = e.toString();
    yourajax.post({
        "url":"/searchSubmit",
        "data":{"content":finalContent},
        "success":function(callback){
            if (callback.code === 200 ){
                var data = callback.data.legends;
                console.log("data",data);
                var module = $('.search_show');
                console.log("module",module);
                var temp = template('template_each',{"template_legends":data});

                module.prepend(temp)
            }
        }
    });
};

Dragen.prototype.onSubmitSearch = function(){
    var self = this;

    self.btnSubmit.click(function(event){
        event.preventDefault();
        var content = self.formtable.find("input[name='content']").val();
        self.ax(content)
    });
    self.btn1.click(function(event){
        event.preventDefault();
        self.ax('1.76')
    });
    self.btn2.click(function(event){
        event.preventDefault();
        self.ax('1.80')
    });
    self.btn3.click(function(event){
        event.preventDefault();
        self.ax('复古')
    });
    self.btn4.click(function(event){
        event.preventDefault();
        self.ax('单职业')
    });
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