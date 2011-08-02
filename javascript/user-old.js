var querylistLength;

function saveThing(e) {
    q = document.search.q.value
        min = document.search.Min.value
        max = document.search.Max.value 
        // Use this current searched-for date as the search_date
	var now = new Date();
    var time
	if (now.getMonth() < 10) {
	    time = $.format.date(now, "yyyy-0MM-dd hh:mm:ss");
	} else {
	    time = $.format.date(now, "yyyy-MM-dd hh:mm:ss")
		}
    
    window.location = '/save?term=' + q.toString() + '&Min=' + min + '&Max=' + max + '&Search_Date=' + time;
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
    //alert(querysize);
    if (querysize < 1) {
	div.parent().parent().parent().parent(".stream_container").fadeOut(function(){$(accordion).append(no_queries)}); 
    } else {
	div.parent().parent().parent().parent(".stream_container").fadeOut(); 
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
	querysize = $('.stream').size();
	
	$(".hideFresh").click(function () { 
		//alert('This would stop the thing from accordioning');
		return false;
	    });

	no_results = "<p class='EmptyResultsText'><b>Sorry, there don't seem to be any fresh results right now</b></p></div>"
	    no_queries = "<p class='EmptyResultsText'><b>Sorry, you don't seem to be any saved searches right now</b></p></div>"
	    $(function() {
		    $("#accordion").accordion({
			    active: false,
			    header: '.stream',
			    autoHeight: false,
			    event: "click",
			    collapsible: true,
			        
			});
		});
	
	$(".x").click(function () { 
		//$(this).parent().parent().parent().parent().parent(".stream_container").fadeOut(); 
	    });
	
    });