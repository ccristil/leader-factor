# Solution MD file

_Use this file as the source of truth for the details of what we're building here_

## Bird's Eye View

- Who is this for: learning managers
  - Bc their involvement is the maiin lever we can pull to increase user engagment
- What the solution does:
  1. Increase visibility for the learning managers
  2. Fit into their existing workflows

## What **IS** the Solution

- Dashboard(increases visibility)
  - Show 3 KPIs
    1. Avg check-in completion _compared to company avg_ | # KPI
       - This is huge because my bet is that competition will increase engagement and get learning managers to _care_ about the progress
       - Won't show specifics of other teams like their indivual plans or check in rate, just the aggregated company rate
       - Green / Red depending on if they are above/below the avg
    2. Who has what each learning commitment is as a table view (sortable) | Bar Chart (with check instatus as series)
    3. Commitments and progress by learner | Table
       - Name, text, status, all sortable
  - In tandem with this, they will get weekly emails (Monday) that show them the Avg check-in completion KPI with a link to the dashboard
    - Email is HTML so it looks clean
    - More on this in the second feature...
  - Features
    - Simple. Clean. Elegant.
    - Use ApexCharts
- Schedule 1 on 1s
  - In the email, have a scheudle one on one button next to each of their learners in a simple table view that will open up a google meet with their email populated into it already and a time selected for the next day at noon or something
    - This fits their existing workflows and pushes them to sign communicate with their learnes about their goals
  - In the dashboard, in KPI #2 have a button embedded beneath each learner's name that does this same thing
  - Features
    - Simple. Clean. Elegant.
    - Keep it concise.
