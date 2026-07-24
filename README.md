# PyGram

Telegram client in Python.

## Obtaining `api_id` and `api_hash`

To obtain an API ID and develop your own application using the Telegram API:

1. Sign up for Telegram using an official Telegram application.
2. Log in at [my.telegram.org](https://my.telegram.org).
3. Go to **API development tools** and fill out the form.
4. You will receive the following credentials:
   - `api_id`
   - `api_hash`

These are required for user authorization.


## Usage

I use this in WSL. You will need Python installed.

Get your credentials from [my.telegram.org](https://my.telegram.org) and add them to your script as `api_id` and `api_hash`.

On a fresh Debian/Ubuntu-based system, run:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv ~/tgvenv
~/tgvenv/bin/pip install --upgrade pip
~/tgvenv/bin/pip install telethon
echo 'alias tg="$HOME/tgvenv/bin/python $HOME/tg.py"' >> ~/.bashrc
source ~/.bashrc
```


Create a file called config.env and place the credentials in as followed:

```
api_id = ABCD1234
api_hash = ABCD1234ABCD1234
```

Then edit your script:

vim ~/tg.py

Make sure it includes your `api_id` and `api_hash`.

Run it with:

`tg`

Notes
This setup assumes your script is saved as `~/tg.py`.
The alias tg runs the script using the Python interpreter inside `~/tgvenv`.
If telethon is missing, install it with:
`~/tgvenv/bin/pip install telethon`
