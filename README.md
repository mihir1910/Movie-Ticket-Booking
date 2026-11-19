# Movie Ticket Booking

A BookMyShow-style web app for browsing movies, finding theatres and shows, and (soon) booking seats.

- **Frontend:** React + Vite, Ant Design, Redux Toolkit, React Router, Axios
- **Backend:** Python, FastAPI, Uvicorn, Motor (async MongoDB driver)
- **Database:** MongoDB Atlas
- **Auth:** JWT stored in an HTTP-only cookie, passwords hashed with bcrypt

---

## What the website does

The app has three kinds of users. Each one sees a different part of the site.

### 1. User (customer)
- Registers and logs in
- Sees all movies on the **Home** page
- Opens a movie to see its details, picks a **date**, and sees which theatres are running that movie and at what times
- Picks a show to book tickets *(the seat selection screen is still being built)*

### 2. Partner (theatre owner)
- Adds their own theatres (name, address, email, phone)
- A new theatre stays **Pending** until an admin approves it
- Adds, edits and deletes **shows** in their theatres: movie, date, time, total seats and ticket price

### 3. Admin
- Adds, edits and deletes **movies** (title, description, language, genre, poster, release date, duration)
- Sees every theatre and can **Approve** or **Block** it

### Pages

| URL | What it shows | Who can open it |
|---|---|---|
| `/login` | Login form | Everyone (logged-in users are sent to `/home`) |
| `/register` | Sign-up form | Everyone |
| `/home` | All movies | Logged-in users |
| `/singleMovie/:id` | Movie details, date picker, theatres and show times | Everyone |
| `/bookshow/:id` | Booking page for one show (in progress) | Everyone |
| `/admin` | Movie list and theatre list tabs | Admin |
| `/partner` | Partner's theatres and their shows | Partner |

Opening `/` takes you to `/home`. If you are not logged in, you go to `/login`.

---

## Project structure

```
Project-movie/
├── .env                  # secrets (you create this, it is not in git)
├── venv/                 # Python virtual environment (you create this)
├── client/               # React frontend
│   └── src/
│       ├── pages/        # Home, Login, Register, SingleMovie, BookShow, Admin/, Partner/
│       ├── components/   # Navbar, MovieCard, ProtectedRoute, PublicRoute
│       ├── calls/        # API calls (axios); backend URL is in calls/config.js
│       └── redux/        # logged-in user state
└── server/               # FastAPI backend
    ├── app.py            # entry point, runs on port 8005
    ├── dbConfig.py       # MongoDB connection
    ├── routes/           # user, movie, theatre, show APIs
    ├── controllers/
    ├── middlewares/      # JWT auth check
    ├── models/           # Pydantic models
    └── requirements.txt
```

---

## Requirements

Install these first:

| Tool | Version | Download |
|---|---|---|
| Python | 3.10 or newer (3.12 recommended) | https://www.python.org/downloads/ |
| Node.js | 20.19+ or 22.12+ (needed by Vite 8) | https://nodejs.org/ |
| Git | any | https://git-scm.com/downloads |

You also need a free **MongoDB Atlas** account: https://cloud.mongodb.com

Check that they are installed:

```bash
python3 --version     # Windows: python --version
node --version
npm --version
git --version
```

---

## Step 1: Get the code

```bash
git clone https://github.com/mihir1910/Movie-Ticket-Booking.git Project-movie
cd Project-movie
```

---

## Step 2: Set up MongoDB Atlas

1. Log in to https://cloud.mongodb.com and create a free **M0** cluster.
2. **Database Access** → add a database user with a username and password.
3. **Network Access** → add your IP address. For local testing you can add `0.0.0.0/0` to allow access from anywhere.
4. On your cluster, click **Connect → Drivers** and copy the connection string. It looks like this:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<username>` and `<password>` with your user's details, and **add a database name after `.net/`**. The backend uses whatever database the URL names, so it must be there:
   ```
   mongodb+srv://myuser:mypassword@cluster0.xxxxx.mongodb.net/BookMyShow?retryWrites=true&w=majority
   ```

---

## Step 3: Create the `.env` file

Create a file named `.env` in the **project root**, the `Project-movie/` folder itself, not inside `server/`:

```env
MONGO_URL=mongodb+srv://myuser:mypassword@cluster0.xxxxx.mongodb.net/BookMyShow?retryWrites=true&w=majority
JWT_SECRET=any_long_random_string
```

- `MONGO_URL` is the connection string from Step 2.
- `JWT_SECRET` can be any long random text. It is used to sign login tokens.

Never commit this file. It is already listed in `.gitignore`.

---

## Step 4: Run the backend

Open a terminal in the `Project-movie/` folder.

### macOS / Linux

```bash
# first time only: create the virtual environment and install packages
python3 -m venv venv
source venv/bin/activate
pip install -r server/requirements.txt

# every time
source venv/bin/activate
cd server
python app.py
```

### Windows: Command Prompt (cmd)

```bat
:: first time only
python -m venv venv
venv\Scripts\activate
pip install -r server\requirements.txt

:: every time
venv\Scripts\activate
cd server
python app.py
```

### Windows: PowerShell

```powershell
# first time only
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r server\requirements.txt

# every time
venv\Scripts\Activate.ps1
cd server
python app.py
```

> **PowerShell says "running scripts is disabled on this system"?** Run this once, then try again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

> **Windows says `python` is not recognized?** Try `py` instead (`py -m venv venv`), or reinstall Python and tick **"Add python.exe to PATH"** on the first installer screen.

When you activate the venv, your prompt starts with `(venv)`. If the server started correctly, you will see:

```
Server is running on port 8005
INFO:     Uvicorn running on http://0.0.0.0:8005
```

Open http://localhost:8005 in a browser. It should say `Hello from Server!`.

Leave this terminal running.

---

## Step 5: Run the frontend

Open a **second** terminal in the `Project-movie/` folder. These commands are the same on macOS, Linux and Windows:

```bash
cd client
npm install       # first time only
npm run dev
```

You will see:

```
VITE ready in ... ms
➜  Local:   http://localhost:5173/
```

Open **http://localhost:5173** in your browser.

---

## Step 6: Make an admin and a partner

Everyone who signs up on `/register` gets the `user` role. To try the admin or partner screens, change the role by hand:

1. Register an account on the website.
2. In MongoDB Atlas, open your cluster → **Browse Collections** → your database → `users`.
3. Find your user, click edit, and change `role` from `"user"` to `"admin"` or `"partner"`.
4. Log out and log in again on the website. Click your name in the navbar to open the admin or partner page.

A good way to test everything:
1. **Admin** adds a few movies.
2. **Partner** adds a theatre.
3. **Admin** approves that theatre.
4. **Partner** adds shows for a movie in that theatre.
5. **User** opens the movie, picks the show's date, and sees the theatre and show times.

---

## Stopping the app

- Press `Ctrl + C` in each terminal.
- Type `deactivate` to leave the Python virtual environment.

---

## API overview

The backend runs at `http://localhost:8005`. FastAPI also gives you interactive API docs at **http://localhost:8005/docs**.

| Area | Prefix | Endpoints |
|---|---|---|
| Auth | `/api/auth` | `POST /register`, `POST /login`, `GET /current-user` |
| Movies | `/api/movie` | `POST /add-movie`, `PUT /update-movie`, `DELETE /delete-movie/{id}`, `GET /all-movies`, `GET /{id}` |
| Theatres | `/api/theatre` | `POST /add-theatre`, `GET /get-all-theatres`, `POST /get-all-theatres-by-owner`, `PUT /update-theatre`, `PUT /delete-theatre` |
| Shows | `/api/shows` | `POST /add-show`, `POST /delete-show`, `PUT /update-show`, `POST /get-all-theatres-by-movie`, `POST /get-show-by-id`, `POST /get-all-shows` |

The full list with request bodies is at http://localhost:8005/docs.

---

## Troubleshooting

### Blank white page at `localhost:5173`
- Check that `npm run dev` is still running.
- Open the browser console (`F12` → Console) and look for red errors.
- Make sure the backend is running on port 8005.

### `DB Connection Failed ... The DNS query name does not exist`
The cluster address in `MONGO_URL` is wrong, or the cluster was deleted or paused. Atlas pauses free clusters that are not used for a long time. Copy a fresh connection string from Atlas (Step 2) and paste it into `.env`.

### `DB Connection Failed ... bad auth` / `Authentication failed`
The username or password in `MONGO_URL` is wrong. If the password contains special characters such as `@`, `#` or `/`, URL-encode them (for example, `@` becomes `%40`), or choose a password with only letters and numbers.

### `DB Connection Failed ... timed out`
Your IP address is not allowed in Atlas. Add it under **Network Access** (Step 2).

### `KeyError: 'MONGO_URL'` or `KeyError: 'JWT_SECRET'`
The `.env` file is missing or in the wrong folder. It must be in `Project-movie/`, not in `server/`.

### `ModuleNotFoundError: No module named 'fastapi'`
The venv is not active. Activate it (Step 4) and run `pip install -r server/requirements.txt` again.

### `address already in use` / port 8005 is busy
Another server is already running on port 8005. Stop it:

- **macOS / Linux**
  ```bash
  lsof -ti :8005 | xargs kill
  ```
- **Windows**
  ```bat
  netstat -ano | findstr :8005
  taskkill /PID <the_number_in_the_last_column> /F
  ```

### CORS errors in the browser console, or API calls fail
Open the site at `http://localhost:5173`, not `http://127.0.0.1:5173`. The backend only accepts requests from `http://localhost:5173` (set in `server/app.py`).

### `on_event is deprecated` warning
This is only a warning from FastAPI. The server still works.
