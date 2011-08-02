
var querylistLength;

function saveThing(e) {
    q = document.search.q.value
        min = document.search.Min.value
        max = document.search.Max.value 
        city = document.search.City.value
        // Use this current searched-for date as the search_date
	var now = new Date();
    var time
	if (now.getMonth() < 10) {
	    time = $.format.date(now, "yyyy-0MM-dd hh:mm:ss");
	} else {
	    time = $.format.date(now, "yyyy-MM-dd hh:mm:ss")
		}
    
    window.location = '/save?term=' + q.toString() + '&Min=' + min + '&Max=' + max + '&Search_Date=' + time + '&City=' + city;
}

function removeFresh(num, div, key) {
    $.ajax({url: '/removeFresh?q='+key,context: document.body,type: 'POST'});
    div.parent().fadeOut();
    $('.results-' + num).fadeOut(function() {
	    $('.results-' + num).empty();
	    $('.results-' + num).append(no_results);
	});    
	
}


function removeQuery(key, div) {
    querysize--;
    $.ajax({url: '/removeQuery?q='+key,context: document.body,type: 'POST'});
    if (querysize < 1) {
	$(accordion).accordion('disable');
	div.fadeOut(function(){$(accordion).accordion('enable');$(accordion).append(no_queries)});
    } else {
	$(accordion).accordion('disable');
	div.fadeOut(function(){$(accordion).accordion('enable');});
    }
    
}

function removeEntry(num, div, q, p) {
    $.ajax({url: '/removeEntry?q=' + q + '&p=' + p,context: document.body,type: 'POST'});
    counterObj = $('.counter-'+num);
    count = counterObj.html() - 1;
    counterObj.html(count);
    
    if (count < 1) {
	div.parent().fadeOut();
	$('.fresh-counter-' + num).fadeOut(function(){
		div.parent().parent().append(no_results);
	    });
    } else {
	div.parent().fadeOut();
    }
}

$(document).ready(function(){
	// Placeholders for divs after deletion
	no_results = "<p class='EmptyResultsText'><b>Sorry, there doesn't seem to be any fresh results right now</b></p></div>";
	no_queries = "<p class='EmptyResultsText'><b>You don't seem to be any saved searches right now</b></p></div>";
	$('.hide_nav').hide();
	
	querysize = $('.stream').size();
	
	// Check to make sure Queries exist
	if ($(accordion).children().size() < 1) {
	    $(accordion).append(no_queries);
	}
	
	// This keeps the accordion from folding
	$(".hideFresh").click(function () { 
		return false;
	    });
	
	$(function() {
		    $("#accordion").accordion({
			    active: false,
				header: '.stream',
				autoHeight: false,
				event: "click",
				collapsible: true,
				
				});
		});
	
    });
