You are a product owner writing user stories for a small development team.

Context:
I am extending an existing Task Tracker web application with a Python/FastAPI backend and a simple web frontend.

Existing features:
- Create tasks with title, description, status (ToDo, InProgress, Done), priority (Low, Medium, High), and assignee.
- View all tasks in a list.
- Filter tasks by status and priority.
- Update task details, including status.
- Delete tasks.

New features to add:

1. Due Dates + Overdue Filter
Expected functionality:
- Tasks can optionally have a due date.
- Users can set a due date when creating or editing a task.
- Users can see the due date on task cards.
- The application should identify overdue tasks.
- Users should have a way to filter or identify overdue tasks.

2. Tags / Labels
Expected functionality:
- Tasks can have multiple tags/labels.
- Users can add tags when creating or editing a task.
- Tags should be displayed on task cards.
- Users can filter or search tasks by tag.

Important constraints:
- Do not add features outside the scope of these two enhancements.
- Do not introduce authentication, user accounts, notifications, reminders, mobile applications, real-time updates, or advanced project management features.
- Keep compatibility with the existing Task Tracker scope.
- Do not assume storage changes, APIs, or UI components unless required by the feature.
- If a design decision is needed (for example, where overdue calculation should happen), mention it as an assumption or decision point.

Target user:
A solo developer or small team managing work in a single shared task list.

Task:
Generate user stories for the two new features:
- Due Dates + Overdue Filter
- Tags / Labels

Generate 3-4 user stories per feature.

User story format:
As a [role], I want [feature] so that [benefit].

Constraints:
- Use "team member" as the main role unless another role is clearly needed.
- Each user story must include 2-3 acceptance criteria that are specific, clear, and testable.
- Include both successful scenarios and failure/validation cases.
- Cover backend behavior, frontend behavior, and user interactions where applicable.
- Do not write technical implementation details or code.
- Do not invent functionality that is not required.

Acceptance criteria should cover examples such as:
- Valid due date creation.
- Invalid date handling.
- Updating due dates.
- Detecting overdue tasks.
- Filtering overdue tasks.
- Adding tags.
- Rejecting empty or invalid tags.
- Updating tags.
- Filtering tasks by tag.
- Keeping existing behavior unchanged for tasks without due dates or tags.

Output format:
Return a table with columns:

| ID | Feature | Story | Acceptance Criteria | Notes / Assumptions |

Include any important product decisions or assumptions in the Notes / Assumptions column.

#######################################################################################################

You are a senior backend developer helping me write Architecture Decision Records (ADRs) for a learning project.

Context:
I am extending an existing Task Tracker application with a Python/FastAPI backend and a simple web frontend.

Reviewed requirements:
<<<
the user stories >>>

Constraints:
- This is a learning project, not production software.
- The backend uses Python, FastAPI, and Pydantic for validation.
- The frontend is a simple web application.
- Keep the architecture simple, easy to understand, and easy to maintain.
- No authentication or user accounts.
- No microservices, Docker, cloud deployment, caching, messaging systems, or production infrastructure.
- Do not introduce functionality that is not required by the supplied user stories.
- Base every architectural decision only on the requirements provided.

Task:

Based on the supplied user stories, create **two separate Architecture Decision Records (ADRs)**—one for each feature:

1. ADR: Due Dates & Overdue Filter
2. ADR: Tags / Labels

For each ADR include:

1. Title
2. Status (Proposed)
3. Context
   - Summarize the relevant user stories.
   - Explain the problem the feature introduces.

4. Decision
   - Describe the chosen approach.
   - Explain why it best fits this project.
   - Clearly state any assumptions.

5. Alternatives Considered
   - Describe at least two reasonable alternatives.
   - Explain why they were not selected.

6. Consequences
   - Benefits
   - Drawbacks
   - Future considerations

7. Impact
   - Backend changes
   - Frontend changes
   - API changes
   - Data model changes
   - Validation requirements
   - Testing impact

Constraints:
- Keep the ADRs concise but complete.
- Follow standard ADR structure.
- Do not include implementation code.
- Do not invent requirements beyond the supplied user stories.
- If a design choice is not specified in the stories (for example, how overdue is calculated or how tags are stored), explicitly document it as an architectural decision and explain the reasoning.

Output format:

Return two clearly separated sections:

# ADR-001: Due Dates & Overdue Filter

...

# ADR-002: Tags / Labels

...