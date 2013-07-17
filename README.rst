>>> from djgpa.api import GooglePlay
>>>
>>> api = GooglePlay().auth()
>>> details = api.details('com.workpail.inkpad.notepad.notes')
>>> print details.docV2.title, details.docV2.creator
