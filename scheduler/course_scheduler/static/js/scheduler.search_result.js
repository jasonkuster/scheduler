function Add(eventID, studentID)
{
	$.post("/scheduler/add_course/", { 'eventID' : eventID, 'studentID' : studentID }, AddSuccess);	
}

function AddSuccess(data, textState, jqXHR)
{
	$('#calendar').fullCalendar('refreshEvents');
	setRemoveButton(data.eventID, data.studentID);
}

function Remove(eventID, studentID)
{
	$.post("/scheduler/remove_course/", { 'eventID' : eventID, 'studentID' : studentID }, RemoveSuccess);	
}

function RemoveSuccess(data, textState, jqXHR)
{
	$('#calendar').fullCalendar('refreshEvents');
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
	$("#info-".concat(eventID)).show();
}

function HideInfo(eventID)
{
	$("#info-".concat(eventID)).hide();
}