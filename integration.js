// code source
// https://www.js-tutorials.com/jquery-tutorials/reading-csv-file-using-jquery/

$(document).ready(function () {
    var data;
    $.ajax({
        // type: "GET",
        // url: "https://github.coecis.cornell.edu/cch227/immunizationeconomics-opportunities.github.io/blob/master/JSI_Data.csv",
        dataType: "text",
        success: function (response) {
            upload();
            data = $.csv.toArrays(response);
            generateHtmlTable(data);
        }
    });

    function upload() {
        var method = "GET";
        var url = "JSI_Data.csv";

        var xhr = new XMLHttpRequest();

        xhr.open(method, url);

        xhr.setRequestHeader("Access-Control-Allow-Origin", "*");

        var text = { "command": "PUSH" };
        xhr.send(text);

    }

    function generateHtmlTable(data) {
        var html = '<table  class="jobs-table">';

        if (typeof (data[0]) === 'undefined') {
            return null;
        } else {
            $.each(data, function (index, row) {
                //bind header
                if (index == 0) {
                    html += '<thead>';
                    html += '<tr>';
                    $.each(row, function (index, colData) {
                        html += '<th>';
                        html += colData;
                        html += '</th>';
                    });
                    html += '</tr>';
                    html += '</thead>';
                    html += '<tbody>';
                } else {
                    html += '<tr>';
                    $.each(row, function (index, colData) {
                        html += '<td>';
                        html += colData;
                        html += '</td>';
                    });
                    html += '</tr>';
                }
            });
            html += '</tbody>';
            html += '</table>';
            alert(html);
            $('#csv-display').append(html);
        }
    }
});