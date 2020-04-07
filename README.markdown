# stagtime

Simple standalone usage:

    python -m stagtime

You probably want to pipe this into something that catches your attention:

    python -m stagtime | while read; do afplay /System/Library/Sounds/Purr.aiff; done

I personally have the following command run on startup:

    tmux new -d -s tagtimed -- 'cd ~/stagtime/; python -m stagtime | while read line; do echo "$line"; for _ in {1..3}; do afplay /System/Library/Sounds/Purr.aiff; done; done; bash'
