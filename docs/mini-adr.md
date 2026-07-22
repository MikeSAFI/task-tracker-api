Mini-ADR-001: Due Dates & Overdue Filter
Status

Accepted

Decision

Store an optional due_date with each task and calculate whether a task is overdue dynamically whenever tasks are retrieved or filtered.

The overdue status is not stored in the task because it can always be derived from the current date and the task's due date. This keeps the data model simple and avoids maintaining duplicate information.

Alternatives Considered
Alternative 1 – Store an overdue field

AI suggested storing an additional Boolean field to indicate whether a task is overdue.

Rejected because:

It duplicates information already available from the due date.
It would require updating the field whenever the current date changes.
It adds unnecessary complexity for a learning project.

Alternative 2 – Manual overdue flag

AI suggested allowing users to manually mark tasks as overdue.

Rejected because:

The overdue state should be determined automatically from the due date.
Manual updates could become inaccurate.
It does not meet the user story requirements.
Outcome

The implementation adds an optional due date, calculates overdue status dynamically, and supports filtering overdue tasks without changing the existing task workflow.


Mini-ADR-002: Tags / Labels
Status

Accepted

Decision

Store tags as an optional collection of strings within each task. Each tag is validated to ensure it:

is not empty,
contains only letters and numbers,
has a maximum length of 255 characters.

This approach keeps the feature simple while satisfying all user story requirements.

Alternatives Considered
Alternative 1 – Separate Tag entity

AI suggested creating a dedicated Tag model with relationships between tasks and tags.

Rejected because:

It introduces additional models and relationships.
It is unnecessary for a simple learning application.
The user stories do not require reusable or managed tags.

Alternative 2 – Single comma-separated string

AI suggested storing all tags as one text field separated by commas.

Rejected because:

Validation becomes more difficult.
Updating individual tags is less straightforward.
Filtering is more cumbersome than using a collection.
Outcome

The implementation allows each task to have multiple optional tags, validates every tag according to the specified rules, displays tags on task cards, and supports filtering tasks by tag while keeping the architecture simple and easy to understand.