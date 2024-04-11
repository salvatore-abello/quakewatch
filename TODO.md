# Completed
+ Switch to gunicorn (or uvicorn if switching to fastapi)
+ Switch from flask to fastapi
+ Remove Flask-jwt-extended, Flask-limiter. Find an alternative
+ Use slowapi instead of Flask-Limter
+ Return number of remaining requests

# TODOs
- Complete register.html
- Complete map.html (use the actual API instead of an external one)
- Fix navbars (add mobile support)
- Add weekly/dayly earthquake visualization (map.html)
- Add CAPTCHA support to (register, frontend and backend)
- Add free/paid js map file
- Improve OpenAPI/Swagger API documentation (https://stackoverflow.com/questions/68815761/how-to-customize-fastapi-request-body-documentation)
- Remove useless files (`__pycache__`, etc...)
- Remove useless import(s)
- Improve backend/frontend source code
- Production
    - Minimize js files
    - Change secrets in .env
    - Obfuscate paid/free js map files using https://www.preemptive.com/online-javascript-obfuscator/

# Other
- Improve the dashboard?
