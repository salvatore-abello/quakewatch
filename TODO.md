# Completed
+ Switch to gunicorn (or uvicorn if switching to fastapi)
+ Switch from flask to fastapi
+ Remove Flask-jwt-extended, Flask-limiter. Find an alternative
+ Use slowapi instead of Flask-Limter
+ Return number of remaining requests
+ Complete register.html
+ Add CAPTCHA support to (register, frontend and backend)
+ Check for expiration date
+ Complete plans.html
+ Change redis.py to redis_client.py
+ Fix navbars (add mobile support)
+ Add support to /query/history/earthquake
+ Complete map.html (use the actual API instead of an external one)
+ Add weekly/daily earthquake visualization (map.html)
+ Add free/paid js map file
+ Use jQuery instead of dcument.querySelector
+ Improve OpenAPI/Swagger API documentation (https://stackoverflow.com/questions/68815761/how-to-customize-fastapi-request-body-documentation)
+ Remove useless files (`__pycache__`, etc...)
+ Remove useless import(s)


# TODOs
- Improve backend/frontend source code
- Production
    - Minimize js/css/html(?) files (https://www.digitalocean.com/community/tools/minify) (https://www.toptal.com/developers/cssminifier) (https://www.atatus.com/tools/html-minify)
    - Change secrets in .env
    - Obfuscate paid/free js map files using https://www.preemptive.com/online-javascript-obfuscator/

# Other
- Improve the dashboard?
