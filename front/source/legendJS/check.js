function Check() {
    var self = this;
    this.cleanAllOfSpider = $("#cleanAllOfSpider");
    this.cleanWebDate = $("#cleanWebDate");
    this.spiderStart = $("#spiderStart");

}


Check.prototype.onBTNclick = function(){
    var self = this;
    self.cleanAllOfSpider.click(
        function(){

        }
    )
};



Check.prototype.Run = function(){
    this.onBTNclick()
};

$(function(){
    var check = new Check();
    check.Run()
});
