# FROM python:3.11

# ENV HOME=/home/fast \
#     APP_HOME=/home/fast/app \
#     PYTHONPATH="$PYTHONPATH:/home/fast" \
#     PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1

# RUN mkdir -p $APP_HOME \
#     && groupadd -r fast\
#     && useradd -r -g fast fast

# WORKDIR $HOME
# COPY . .
# ADD alembic.ini .

# RUN pip install --upgrade pip && pip install -r app/req.txt && chown -R fast:fast .
# COPY . .

# USER fast