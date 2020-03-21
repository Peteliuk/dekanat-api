# dekanat-api
## API for dekan.at android app

[**dekanat-api.herokuapp.com**](https://dekanat-api.herokuapp.com)

### Description
API for bachaleur work - Android voice assistant for university called "dekan.at".    
API based on [schedule-API](https://github.com/thestd/schedule-API). It gets subjects lists for all groups of Mathematic & Informatic faculty of Precarpathian National University for a 1 day and allows you to ask some difficult queries, for example: "where free audithorium", and get list of audithoriums without subjects at current time. API gets your current time in "%H:%M" format (like 19:52) and convert it into subjects number, for example if time is 11:00, subject number will be 2 or 3 (I don't remember, but API does :) ).    
API has own database which updates every hour.

### Usage
Now you can make queries like:    
    `/api/where_subject/group=<string:group_name>&time=<string:current_time>`
    `/api/where_free_auditorium/time=<string:current_time>`
    `/api/what_teacher/group=<string:group_name>&time=<string:current_time>`
    `/api/what_subject/group=<string:group_name>&time=<string:current_time>`
    `/api/is_teacher_here/teacher=<string:teacher_name>`

****
**In development**