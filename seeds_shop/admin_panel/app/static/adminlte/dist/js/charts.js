function calculateSum(arr) {
    var sum = 0;
    for (var i = 0; i < arr.length; i++) {
        sum += arr[i];
    }
    return sum;
}

document.addEventListener("DOMContentLoaded", function () {
    let context = $("#stat_chart").get(0).getContext('2d');

    let labels = JSON.parse(context.canvas.dataset.dates);
    console.log(context.canvas.dataset);
    let registered_users = JSON.parse(context.canvas.dataset.registered_users);
    let orders_created = JSON.parse(context.canvas.dataset.orders_created);
    let products_puchased = JSON.parse(context.canvas.dataset.products_puchased);
    let tickets_opened = JSON.parse(context.canvas.dataset.tickets_opened);

    let chart
    chart = new Chart(context, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: "Зарегистрировано пользователей",
                data: registered_users,
                fill: true,
                lineTension: 0.2,
                backgroundColor: "rgba(54, 162, 235, 0.5)",
                borderColor: "rgb(54, 162, 235)",
                borderWidth: 1.2
            },
                {
                    label: "Создано заказов",
                    data: orders_created,
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(160, 64, 255, 0.5)",
                    borderColor: "rgb(160, 64, 255)",
                    borderWidth: 1.2
                },
                {
                    label: "Куплено товаров",
                    data: products_puchased,
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(48, 198, 124, 0.5)",
                    borderColor: "rgb(48, 198, 124)",
                    borderWidth: 1.2
                },
                {
                    label: "Открыто тикетов",
                    data: tickets_opened,
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(255, 51, 51, 0.5)",
                    borderColor: "rgb(255, 51, 51)",
                    borderWidth: 1.2
                },
            ]
        },
        options: {
            responsive: true
        },
    })

    $("#changeDateButton").click(() => {
        let data = {date_from: $('#datefrom').val(), date_to: $('#dateto').val()};
        var response = $.post(window.location.href, data)
        response.done(function (chartData) {
            chart.data.labels = chartData[0]
            chart.data.datasets[0].data = chartData[1].registered_users
            chart.data.datasets[1].data = chartData[1].orders_created
            chart.data.datasets[2].data = chartData[1].products_puchased
            chart.data.datasets[3].data = chartData[1].tickets_opened
            chart.update();

            try {
                $("#registered_users").text(calculateSum(chartData[1].registered_users));
                $("#orders_created").text(calculateSum(chartData[1].orders_created));
            } catch (e) {
                console.log(e);
            }

            $('#table_stats').find('tbody')[0].innerHTML = '';
            var dates = chartData[0];
            var column_data = chartData[1].table_rows;
            var rows_sums = chartData[1].rows_sums;

            var tab = []
            for (var i = 0; i < column_data.length - 1; i++) {
                tab += '<tr>'
                tab += '<td>' + dates[i] + '</td>'
                column_data[i].forEach(function (item) {
                    tab += '<td>' + item + '</td>'
                })
                tab += '</tr>'
            }

            tab += '<tr>'
            tab += '<td> Всего: </td>'
            rows_sums.forEach(function (item) {
                tab += '<td>' + item + '</td>'
            })

            tab += '</tr>'

            $('#table_stats').find('tbody')[0].innerHTML = tab;
        });
    });
});
