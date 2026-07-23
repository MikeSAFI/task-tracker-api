ID	Feature	Story	Acceptance Criteria	Notes / Assumptions

US-DD-01	Due Dates + Overdue Filter	As a team member, I want to set an optional due date when creating a task so that I can track when work needs to be completed.	
1. When creating a task, a valid due date that is today or a future date can be provided and the task is saved with that due date.
2. When no due date is provided, the task is created successfully and behaves the same as existing tasks.
3. If an invalid date value is entered, the task creation is rejected with a clear validation message.	
Due dates are optional. Existing tasks without due dates must continue working without changes. Date format and timezone handling should follow the application's existing conventions.Due dates cannot be earlier than the current date.

US-DD-02	Due Dates + Overdue Filter	As a team member, I want to view and update a task's due date so that I can keep task deadlines accurate when priorities change.	
1. A task card displays the assigned due date when one exists.
2. A team member can edit an existing task and change or remove its due date.
3. Updating a due date does not modify other task information such as title, status, priority, or assignee.	
Removing a due date should return the task to a state where no deadline is assigned. No additional reminder functionality is included.

US-DD-03	Due Dates + Overdue Filter	As a team member, I want the application to identify overdue tasks so that I can focus on tasks that have passed their deadlines.	
1. A task with a due date earlier than the current date is identified as overdue.
2. A task with no due date is not considered overdue.
3. A task with a due date equal to the current date is not marked overdue unless the product later defines time-based overdue rules.	
Overdue calculation is a product decision point. Assumption: overdue status is calculated based on the current date, not a specific time of day.

US-DD-04	Due Dates + Overdue Filter	As a team member, I want to filter tasks by overdue status so that I can quickly find tasks that need attention.	
1. Selecting the overdue filter displays only tasks that are identified as overdue.
2. Tasks without due dates or tasks that are not overdue are excluded from the overdue results.
3. Clearing the overdue filter restores the normal task list behavior.	
The overdue filter should work alongside existing task filtering without changing existing status or priority filters.

Notes: In US-DD-01 AI didnt mention what a valid due date is, so i asked it to fix this story to include that due date cannot be earlier than the current date. 
################################################
ID	Feature	Story	Acceptance Criteria	Notes / Assumptions

US-TAG-01	Tags / Labels	As a team member, I want to add multiple tags to a task so that I can categorize and organize tasks more easily.	
1. A team member can add one or more valid tags when creating a task.
2. Added tags are displayed on the task card.
3. A task can be created without tags and continues to work like existing tasks.	Tags are optional. No predefined tag list or tag management feature is required.
US-TAG-02	Tags / Labels	As a team member, I want to update or remove task tags so that task categories remain accurate over time.	
1. A team member can add new tags while editing an existing task.
2. A team member can remove existing tags from a task.
3. Updating tags does not change other task fields such as title, status, priority, or assignee.	Tags only apply to individual tasks. No global tag administration is included.

US-TAG-03	Tags / Labels	As a team member, I want tags to follow validation rules so that task labels remain consistent, clean, and easy to search.	
1. A tag cannot be empty, contain only whitespace, or exceed 255 characters in length.
2. A tag containing characters other than letters (A-Z, a-z) and numbers (0-9) is rejected with a clear validation message.
3. Valid tags containing only letters and numbers, with a maximum length of 255 characters, are successfully saved and displayed on the task card.	Tags are stored with a maximum length of 255 characters (VARCHAR(255)). Tags support only alphanumeric characters (letters and numbers). Spaces, symbols, and special characters are not allowed. No advanced tag management or predefined tag list is introduced.

US-TAG-04	Tags / Labels	As a team member, I want to filter tasks by tag so that I can quickly find related tasks.	
1. Selecting a tag filter displays tasks containing that tag.
2. Tasks without the selected tag are excluded from the filtered results.
3. Clearing the tag filter restores the normal task list behavior.	Tag filtering should work with existing filters (status and priority) without changing current behavior.

Notes: In US-TAG-03 AI didnt mention any validation rules for tags other than empty string so i told it to rewrite the story by adding validation rule so tag can have a maximum length of 255 characters and only accept letters and numbers.