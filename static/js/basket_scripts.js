window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        var basket_link = event.target;
        $.ajax({
            url: "/basket/edit/" + basket_link.name + "/" + basket_link.value + "/",
            success: function (data) {
                $('.basket_list').html(data.result);
            },
        });
    event.preventDefault();
    });

    $('.basket_list').on('click', 'button', function () {
        var basket_link = event.target;
        $.ajax({
            url: "/basket/delete/" + basket_link.name,
            success: function (data) {
                $('.basket_list').html(data.result);
            },
        });
    event.preventDefault();
    });
}