function Input() {
    var self = this;
    self.submitBtn = $(".btn-outline-success");

}


Input.prototype.onSubmitBtn = function(){
    var self = this;
    self.submitBtn.click(function(){

    })
};



Input.prototype.Run = function(){
    this.onSubmitBtn()
};

$(function(){
    var input = new Input();
    input.Run()
});
