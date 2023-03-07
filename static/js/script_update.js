var input = document.getElementById("form_app");
    
    
    function check(){
        if(input.title.value=="" || input.money.value==""){
            alert("必須項目が入力されていません");
            return false;
        }
        if (isNaN(input.money.value)){
            alert("金額は数値で入力する必要があります");
            return false;
        }
        if (input.money.value>=500000){
            //金額が大きいため一度警告を入れる
            let result = window.confirm(input.money.value +'：金額がかなり大きいですがよろしいでしょうか。');

            if(result){
                return true;
            }else {
                return false;
            }
        }

        return true;
    }