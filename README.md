# bitbar-plugins

## Installation

1. Install fantastic bitbar application for mac (https://github.com/matryer/bitbar)
2. Clone this repo
3. Create enabled folder inside bitbar-plugins directory
4. Launch BitBar and select the `enabled` folder in your BitBar preferences.

## Using symlinks

Because Git will ignore everything in `bitbar-plugins/enabled`, you can use it to maintain your own plugins directory while still benefitting from tracking (upstream) changes.

### Example

	cd bitbar-plugins/enabled

	# Enable spotify plugin
	ln -s ../scripts/spotify.10s.sh

	# Enable uptime plugin and change update interval to 30 seconds
	ln -s ../scripts/uptime.1m.sh uptime.30s.sh

Then select the `enabled` folder in your BitBar preferences.

