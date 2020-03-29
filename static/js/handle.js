$(function () {

    $("#checkAll").click(function () {
        if (this.checked == true) {
            $("input[name='subBox']").each(function () {
                this.checked = true;
            })
        }

        if (this.checked == false) {
            $('input[name="subBox"]').each(function () {
                this.checked = false;

            })
        }


    });




    $("#deloy_server").click(function () {
        var deloy_arry = new Array()

        $('input[name="subBox"]:checked').each(function () {

            deloy_arry.push($(this).val())
        })
        console.log("发布", deloy_arry)

        list = {
            "data": "111"
        }
        $.ajax({
            //请求方式
            type: "POST",
            //请求的媒体类型
            contentType: "application/json;charset=UTF-8",
            //请求地址
            url: "{% url 'deloy_server' %}",
            //数据，json字符串
            data: JSON.stringify(list),
            //请求成功
            success: function (result) {
                console.log(result);
            },
            //请求失败，包含具体的错误信息
            error: function (e) {
                console.log(e.status);
                console.log(e.responseText);
            }
        });



    });

    $("#deloy_del").click(function () {
        var del_arry = new Array()

        $('input[name="subBox"]:checked').each(function () {
            del_arry.push($(this).val())


        })
        console.log("删除", del_arry)

    });



    $("#put_content").click(function () {
        $("input").attr({
            disabled: false,

        })
    });




});