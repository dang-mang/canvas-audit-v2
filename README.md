# canvas_audit
This is a piece of software that gets all user information from the Canvas API andThis project is a work in progress, I am currently trying to make it more user friendly.


## How to use
1) You need to make sure that you have python installed with the pandas library.
2) Fill out a file in the directory named "config.py" using the "config_template.py" as a template. You will need your Canvas API key and target URL.
3) Make sure that you have the source document from the Canvas API. It is the one with the first 2 columns as "admin_user_name" and	"canvas_user_id"
4) Run "python3 get_admins.py" 
5) Once that is finished, run "python3 json_to_csv_original.py l input.json admins.csv". If this doesn't work, you may have to validate and fix the JSON with an online tool.

## Future plans
1) Auto formatting for JSON. It's a big sample size, so sometimes if there is an error in the API, in the download, or something else, then you need to auto format it to prevent bugs.
2) Make everything run in 1 command.
