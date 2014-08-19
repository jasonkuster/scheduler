function searchSuccess(data, textState, jqXHR)
{
	var html = new String(data);
	if (html.substring(0, html.indexOf('</span>')).indexOf("'".concat($("#course_search").val()).concat("'")) >= 0)
	{
		$("#search_result").html(data);
	}
}
	
function search()
{	
	if (new String($("#course_search").val()).length > 2)
	{
		$("#search_result").html('<div class="searching-panel">Searching . . .</div>');
		$.get("/scheduler/search/", { 'criterion' : $("#course_search").val() }, searchSuccess, 'html');
	}
	else
	{
		clearResults();
	}
}

function clearResults()
{
	$("#search_result").html('<div></div>');
}