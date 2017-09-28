#!/bin/sh

set -e

# Add python manage.py as command if needed
if [ "$1" = 'runserver' ]; then
	set -- python manage.py "$@"
fi


# Drop root privileges if we are running python manage.py
# allow the container to be started with `--user`
if [ "$1" = 'python' -a "$2" = 'manage.py' -a "$(id -u)" = '0' ]; then
    python manage.py migrate --no-input
	set -- su-exec distribrewed "$@"
fi

# As argument is not related to django,
# then assume that user wants to run his own process,
# for example a `bash` shell to explore this image
exec "$@"