function Add(eventID, studentID)
{
	$.post("/scheduler/add_course/", { 'eventID' : eventID, 'studentID' : studentID }, AddSuccess);	
}

function AddSuccess(data, textState, jqXHR)
{
	$("#calendar").fullCalendar("refetchEvents");
	setRemoveButton(data.eventID, data.studentID);
}

function Remove(eventID, studentID)
{
	$.post("/scheduler/remove_course/", { 'eventID' : eventID, 'studentID' : studentID }, RemoveSuccess);	
}

function RemoveSuccess(data, textState, jqXHR)
{
	$("#calendar").fullCalendar("refetchEvents");
	setAddButton(data.eventID, data.studentID);
}

function setRemoveButton(eventID, studentID)
{
	var eventIDWithoutQuotes = eventID.substring(1, eventID.length - 1);
	$("#button-".concat(eventID)).html("<button class='btn btn-danger btn-xs' onclick='Remove(&quot;"+ eventID +"&quot;,&quot;"+ studentID+"&quot;)'>Remove</button>");
}

function setAddButton(eventID, studentID)
{
	var eventIDWithoutQuotes = eventID.substring(1, eventID.length - 1);
	$("#button-".concat(eventID)).html("<button class='btn btn-success btn-xs' onclick='Add(&quot;"+ eventID +"&quot;,&quot;"+ studentID+"&quot;)'>Add</button>");
}

function ToggleInfo(eventID)
{
	if ($("#info-".concat(eventID)).is(":visible"))
	{
		HideInfo(eventID);
	}
	else
	{
		ShowInfo(eventID);
	}
}

function ShowInfo(eventID)
{
	$("#info-".concat(eventID)).slideDown();
}

function redraw(elementID)
{
	var element = document.getElementById(elementID);
	var n = document.createTextNode(' ');
	var disp = element.style.display;  // don't worry about previous display style
	 
	element.appendChild(n);
	element.style.display = 'none';
	 
	setTimeout(function(){
	    element.style.display = disp;
	    n.parentNode.removeChild(n);
	},20);
}

function HideInfo(eventID)
{
	$("#info-".concat(eventID)).slideUp();
	redraw("#info-".concat(eventID));
}

