This is Not LinkedIn API
========================

kapi-python is [This is Not LinkedIn's](https://thisisnotlinkedin.com/) API for downloading and uploading all your resumes and availability documents.

You can easily edit your own resume and availability locally in text files, add your profiles to source control, and upload your changes directly from the command line.

kapi-python includes a simple command line client so you can use the API without needing to write any code yourself.

Features
--------

- View your resumes as JSON
- Download your resumes as JSON
- Upload resumes to your account

- View your availability as JSON
- Download your availability as JSON
- Upload availability to your account


Getting Started
---------------

```shell
$ pipenv sync
```

Commands
--------

- `init`
    - Save your API key so commands can access your account
    - You can generate an API key by logging in to [This Is Not LinkedIn](https://thisisnotlinkedin.com) going to "Edit Profile" then clicking on "Add API Key"

```shell
$ pipenv run ./cli.py init
```

- `resume`
    - `get [personality] [[name]]` - retrieve all resumes under `personality`. If `name` also provided, only return specific resume.
    - `list` - print all resumes under all personalities to console
    - `list --save` - save all resumes to files inside directories with personality names
    - `list --save --overwrite` - save all resumes while replacing all existing files (by default files are preserved)
    - `save [resume-name.json]` - upload resume using the personality-directory file system layout created by `--save` (directory name will be used for the personality name; resume name will be the filename with `.json` removed)
    - `upload [personality] [resume-name] [file-name.json]` - upload resume to arbitrary personality and resume name from a source file (does not require the specific directory and filename layout of `save` command)

```shell
$ pipenv run ./cli.py resume list --save
```

- `avail`
    - `list` - print all availability to console
    - `list --save` - save all availability to a directory
    - `list --save --overwrite` - save all availability to a directory, replacing any existing files
    - `save [avail-name.json]` - upload availability where name is auto-detected by removing `.json` from filename

```shell
$ pipenv run ./cli.py avail list --save
```

Current Limitations
-------------------

Currently you must still use the [This is Not LinkedIn](https://thisisnotlinkedin.com) website for:

- creating accounts
- creating availability
- creating personalities
- creating resumes
- requesting API keys
- changing visibility from Hidden (default) to Public
- setting ACL details for resumes (hide employer names by default, hide anything older than X months/years, ...)
- managing TOTP credentials
- changing your display username (your https://thisisnotlinked.com/username/ path)
- subscribing to paid membership for more features (not available yet)


To create and upload a new resume, you'll have to use the website for the "create" portion, but then you can upload to the name you created through the cli/API. Remember to toggle item visibility to Public when you're ready to share with the world.


TODO
----

- Include examples of valid resume and availability documents
    - The easiest way to figure out the format: create new resumes/availability using the website wizards then view the JSON to see what got written. Modify as necessary.
    - There's also JSON Schema output for resumes and availability floating around somewhere on the website if you can find it.
- Allow modifications by API (rename, upload ACLs, delete)
- View / edit / add connections to other personalities / resumes


Contributions
-------------
Want to add features or fix problems? Submit a PR as we'll improve things together.


Thanks
------
kapi-python is modeled after the [stripe-python](https://github.com/stripe/stripe-python) API architecture when it comes to managing API keys and allowing extensible creation of data from API endpoints without needing to first instantiate an API Factory Factory holding credentials.
