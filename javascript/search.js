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
