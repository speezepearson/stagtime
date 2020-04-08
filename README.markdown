# stagtime

Simple standalone usage:

    python -m stagtime

You probably want to pipe this into something that catches your attention:

    python -m stagtime | while read; do afplay /System/Library/Sounds/Purr.aiff; done

I personally have the following command run on startup on OS X:

    tmux new -d -s tagtimed -- 'source ~/.venv/default/bin/activate; python -m stagtime | while read line; do echo "$line"; for _ in {1..3}; do afplay /System/Library/Sounds/Purr.aiff; done; done; bash'

and on Ubuntu:

    tmux new -d -s tagtimed -- 'source ~/.venv/default/bin/activate; python -m stagtime | while read line; do echo "$line"; for _ in {1..2}; do play /usr/share/sounds/ubuntu/notifications/Slick.ogg; done; done; bash'
