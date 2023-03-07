function all_delete_check(){
    let result = window.confirm("全てのデータを削除してもよろしいでしょうか。");

    if(result){
        return true;
    }else {
        return false;
    }
}
