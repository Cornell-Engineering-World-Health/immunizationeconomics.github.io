// US States object
var usStates = [
  'AL',
  'AK',
  'AZ',
  'AR',
  'CA',
  'CO',
  'CT',
  'DE',
  'DC',
  'FL',
  'GA',
  'HI',
  'ID',
  'IL',
  'IN',
  'IA',
  'KS',
  'KY',
  'LA',
  'ME',
  'MD',
  'MA',
  'MI',
  'MN',
  'MS',
  'MO',
  'MT',
  'NE',
  'NV',
  'NH',
  'NJ',
  'NM',
  'NY',
  'NC',
  'ND',
  'OH',
  'OK',
  'OR',
  'PA',
  'RI',
  'SC',
  'SD',
  'TN',
  'TX',
  'UT',
  'VT',
  'VA',
  'WA',
  'WV',
  'WI',
  'WY'
]

// Constant determining how many custom filters there will be
var numFilters = 3;

function checkIfUSState(location) {
  var stateAbbrev = location.substring(
    location.indexOf(",") + 2,
    location.length - 1);
  for (var i = 0; i < usStates.length; i++) {
    if (usStates[i] === stateAbbrev) return true;
  }
  return false;
}

// Create filter based off filter type and name
function createFilter(filterName, id, filterData) {
  var filterCategory = document.createElement('div');
  filterCategory.id = filterName.toLowerCase() + '-dropdown-content'
  filterCategory.className = "filter-dropdown-content";
  for (var i = 1; i < filterData.length; i++) {
    if (document.getElementById(id) === null) {
      var currDiv = document.createElement('div');
      currDiv.id = id;
      document.querySelector('#filters').append(currDiv);
    } else {
      var currDiv = document.getElementById(id);
    }
    var innerDiv = document.createElement('div');
    innerDiv.className = 'cb-input';
    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = 'cb-' + filterData[i];
    checkbox.name = filterName.toLowerCase();
    checkbox.value = filterData[i];
    var checkLabel = document.createElement('label');
    checkLabel.htmlFor = 'cb-' + filterData[i]
    checkLabel.textContent = ' ' + filterData[i].toUpperCase() + ' ';
    currDiv.className = 'filter-category'
    innerDiv.append(checkbox);
    innerDiv.append(checkLabel);
    filterCategory.append(innerDiv);
  }
  var dropDownButton = document.createElement('button');
  dropDownButton.className = 'filter-dropdown-button'
  dropDownButton.textContent = filterName.toUpperCase();
  dropDownButton.onclick = function () {
    document.getElementById(filterName.toLowerCase() + '-dropdown-content').classList.toggle('show-dropdown');
  }
  currDiv.append(dropDownButton);
  currDiv.append(filterCategory);
}

// Create and format datatable

$(document).ready(function () {
  // Show filter options
  $('#filters').removeClass('collapse')
  $('#filters').addClass('show')
  $('#filters').css('display', 'flex');
  // 2D array of filters
  // filters[0] is array of filter names
  // filters[1] is array of job types
  // filters[2] is array of organizations
  // filters[3] is array of locations
  const filters = [];
  for (var i = 0; i < numFilters; i++) filters.push([]);

  // Parse csv file from github
  $.ajax({
    url: "https://raw.githubusercontent.com/Cornell-Engineering-World-Health/immunizationeconomics.github.io/main/JSI_Data.csv",
    dataType: "text",
    success: function (data) {
      var full_job = data.split(/""\r?\n|\r/);
      var table_data = '<table id="job_table" class="display table table-bordered table-striped cell-border">';
      for (var count = 0; count < full_job.length - 1; count++) {
        var cell_data = splitCSV(full_job[count]);
        var len = cell_data.length;

        // Job type
        if (!filters[0].includes(cell_data[4])) filters[0].push(cell_data[4]);

        // Location
        var country = checkIfUSState(cell_data[3]) ? "United States" :
          count > 0 ?
            cell_data[3].substring(cell_data[3].indexOf(" ") + 1,
              cell_data[3].length - 1) :
            cell_data[3].substring(cell_data[3].indexOf(" ") + 1);
        if (!filters[1].includes(country)) filters[1].push(country);

        // Organization
        if (!filters[2].includes(cell_data[len - 1])) filters[2].push(cell_data[len - 1]);
        cell_data.splice(0, 1);
        if (count == 0) {
          table_data += '<thead>';
        }
        else if (count == 1) {
          table_data += '<tbody>';
        }
        table_data += '<tr>';
        for (var cell_count = 0; cell_count < cell_data.length; cell_count++) {
          if (count === 0) {
            if (cell_count == 0 || cell_count == 3 || cell_count == 5) {
              table_data += '<th class="collapse">' + cell_data[cell_count] + '</th>';
            }
            else {
              table_data += '<th>' + cell_data[cell_count] + '</th>';
            }
          }
          else {
            if (cell_count == 1) {
              table_data += '<td><a target="_PARENT" href=' + cell_data[0] + '>' + cell_data[cell_count] + '</a></td>';
            }
            else if (cell_count == 0 || cell_count == 3 || cell_count == 5) {
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

      // Convert csv to html
      $('#job_postings').html(table_data).ready(function () {

        // Configure custom filter for posting type
        $.fn.dataTable.ext.search.push(
          function (settings, searchData, index, rowData, counter) {
            var type = $('input:checkbox[name="type"]:checked').map(function () {
              return this.value;
            }).get();

            if (type.length === 0 || type.length === 2) {
              return true;
            }

            if ((type.indexOf(searchData[3]) !== -1) || searchData[3] === 'Both') {
              return true;
            }

            return false;
          }
        );

        // Configure custom filter for organization
        $.fn.dataTable.ext.search.push(
          function (settings, searchData, index, rowData, counter) {
            var org = $('input:checkbox[name="org"]:checked').map(function () {
              return this.value;
            }).get();

            if (org.length === 0 || org.length === 10) {
              return true;
            }

            if ((org.indexOf(searchData[5]) !== -1)) {
              return true;
            }

            return false;
          }
        );

        // Configure custom filter for location by country
        $.fn.dataTable.ext.search.push(
          function (settings, searchData, index, rowData, counter) {
            var type = $('input:checkbox[name="location"]:checked').map(function () {
              return this.value;
            }).get();

            if (type.length === 0) {
              return true;
            }

            var location = searchData[2].trim();

            var country = checkIfUSState(location) ? "United States" :
              location.substring(
                location.indexOf(",") + 2,
                location.length - 1);
            if (type.length == 1 && type[0] === country) {
              return true;
            }

            return false;
          }
        );

        // Create dataTable object
        var table = $('#job_table').DataTable({
          "columnDefs": [
            {
              "render": function (data, type, row) { return data + ', ' + row[2]; },
              "targets": 1
            },
            { "visible": false, "targets": [2] },
            {
              "targets": 4,
              "render": function (data, type, row) { return data.substr(0, 1000) + '...'; }
            }
          ]
        });

        // Apply table search function to custom search input element
        $('#searchFilter').keyup(function () {
          table.search(this.value).draw();
        });

        // Apply filtering changes if prompted
        $('input:checkbox').on('change', function () {
          table.draw();
        });
      });

    }
  }).then(() => {
    for (var i = 0; i < numFilters; i++) {
      createFilter(filters[i][0], filters[i][0], filters[i]);
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


