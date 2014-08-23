function searchSuccess(data, textState, jqXHR)
{
	if (data.substring(0, data.indexOf('</span>')).indexOf("'".concat($("#course_search").val()).concat("'")) >= 0)
	{
		$("#search_result").empty();
		var html = $.parseHTML(data);
		$(html).each(function(index, element) {
			if ($(element).attr("id") === "result")
			{
				$("#search_result").append(element);
				var $lefty = $(element).next();
				$lefty.animate({
					left: parseInt($lefty.css('left'),10) == 0 ?
							$lefty.outerWidth() :
								0
					});
				});
			}
		});
		//$("#search_result").html(data);
		
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