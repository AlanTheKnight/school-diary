function renderAvg(s) {
    if (s != "-")
        return s.toPrecision(2).replace(".", ",")
    return s;
}

function myfunction(that){
    that.style.backgroundColor = "#d6d6d6"
    that.parentNode.style.backgroundColor = "#d6d6d6"
    // save mark
    let csrf = $("input[name='csrfmiddlewaretoken']").val();
    let id = "button[name='"+ that.name.toString()+"']";
    let comment_btn = $(id);
    if (that.value){
        comment_btn.css("display", "inline");
    }else{
        comment_btn.css("display", "none");
    }
    value = Number(that.value);  // Value of mark
    let mark_data = that.name.split("|").map(x => Number(x))
    $.ajax({
        url: $("input[name='save-mark-url']").val(),
        method: 'POST',
        data:{
            "csrfmiddlewaretoken": csrf,
            "student": mark_data[0],
            "lesson": mark_data[1],
            "value": value,
        },
        success: function (data){
            let sm_avg = $("#s_"+mark_data[0]);
            let avg = $("#"+mark_data[0]);
            sm_avg.html(renderAvg(data.sm_avg));
            avg.html(renderAvg(data.avg));
        }
    })
};

function commentDialog(that) {
    let data = that.name.split("|").map(x => Number(x))
    let csrf = $("input[name='csrfmiddlewaretoken']").val()
    $.ajax({
        url: $("input[name='get-comment-url']").val(),
        method: "POST",
        data: {
            "csrfmiddlewaretoken": csrf,
            "lesson": data[1],
            "student": data[0],
        },
        success: function (data) {
            if (data.status == "aborted") return 
            $("#comment-text").val(data.comment)
            $("#comment-hidden").val(that.name)
            $("#comment-modal").modal('show')
        },
    })
};

function addComment() {
    let commentText = $("#comment-text").val()
    let data = $("#comment-hidden").val().split("|").map(x => Number(x))
    let csrf = $("input[name='csrfmiddlewaretoken']").val()
    $.ajax({
        url: $("input[name='add-comment-url']").val(),
        method: "POST",
        data: {
            "csrfmiddlewaretoken": csrf,
            "comment": commentText,
            "lesson": data[1],
            "student": data[0],
        },
    })
    $("#comment-text").val("")
    $("#comment-modal").modal('hide')
}