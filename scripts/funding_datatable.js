// Create and format datatable

$(document).ready(function () {
  // Show filter options
  $('#filters').removeClass('collapse')
  $('#filters').addClass('show')

  // Parse csv file from github
  $.ajax({
    type: "GET",
    url: "https://raw.githubusercontent.com/Cornell-Engineering-World-Health/immunizationeconomics.github.io/main/Rockefeller_Funding_Data.csv",
    dataType: "text",
    success: function (data) {
      var full_job = data.split(/""\r?\n|\n/);
      var table_data = '<table id="job_table" class="display table table-bordered table-striped cell-border">';
      for (var count = 0; count < full_job.length - 1; count++) {
        var cell_data = splitCSV(full_job[count]);
        var len = cell_data.length;

        if (count == 0) {
          table_data += '<thead>';
        }
        else if (count == 1) {
          table_data += '<tbody>';
        }
        table_data += '<tr>';
        for (var cell_count = 0; cell_count < len; cell_count++) {
          if (count === 0) {
            if (cell_count == 0 || cell_count == 1) {
              table_data += '<th class="collapse">' + cell_data[cell_count] + '</th>';
            }
            else {
              table_data += '<th>' + cell_data[cell_count] + '</th>';
            }
          }
          else {
            if (cell_count == 2) {
              table_data += '<td><a target="_PARENT" href=' + cell_data[1] + '>' + cell_data[cell_count] + '</a></td>';
            }
            else if (cell_count == 0 || cell_count == 1) {
              table_data += '<td class="collapse">' + cell_data[cell_count] + '</td>';
            }
            else {
              table_data += '<td>' + cell_data[cell_count] + '</td>';
            }
          }
        }
        table_data += '</tr>';
        if (count == 0) {
          table_data += '</thead>';
        }
      }
      table_data += '</tbody>';
      table_data += '</table>';
      console.log(table_data)
      // Convert csv to html
      $('#job_postings').html(table_data).ready( function() {
        var table = $('#job_table').DataTable();
      });
    }
  });

});

// split CSV by cell
function splitCSV(str) {
  //split the str first
  //then merge the elments between two double quotes
  var delimiter = ',';
  var quotes = '"';
  var elements = str.split(delimiter);
  var newElements = [];
  for (var i = 0; i < elements.length; ++i) {
    if (elements[i].indexOf(quotes) >= 0) {//the left double quotes is found
      var indexOfRightQuotes = -1;
      var tmp = elements[i];
      //find the right double quotes
      for (var j = i + 1; j < elements.length; ++j) {
        if (elements[j].indexOf(quotes) >= 0) {
          indexOfRightQuotes = j;
          break;
        }
      }
      //found the right double quotes
      //merge all the elements between double quotes
      if (-1 != indexOfRightQuotes) {
        for (var j = i + 1; j <= indexOfRightQuotes; ++j) {
          tmp = tmp + delimiter + elements[j];
        }
        newElements.push(tmp);
        i = indexOfRightQuotes;
      }
      else { //right double quotes is not found
        newElements.push(elements[i]);
      }
    }
    else { //left double quotes is not found
      newElements.push(elements[i]);
    }
  }
  return newElements;
}
