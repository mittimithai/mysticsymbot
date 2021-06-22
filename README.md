# Get Started
Assuming you have python3, cd to the directory of this program, make a venv `python -m venv mysticsymbot-env`.

Activate the venv with `source mysticsymbot-venv/bin/activate`.

Install requirements `pip install -r requirements.txt`.

Edit the config.json file with the rsrc_dir and appropriate auth keys.

Then `python bot_poster.py` will take the top line from `rsrc_dir/to_post.csv` and post the corresponding title and image across each type of bot it has. Done!
