# software-engineering-and-agile-assignment

## Login Credentials

### Admin User

E: admin@admin.com
P: adminadmin

### Regular User

E: regular@user.com
P: regularuser

## Run

Install dependencies via `poetry install`, or use the provided requirements.txt. It is reccomended to use a virtual environment.

To launch the local server run:

```sh
make dev
```

## Format

Black is installed as a development dependency and can be used to auto format python code.

djhtml is installed as a development dependency and can be used to auto format template files.

The following command will format all files:

```sh
make format
```
