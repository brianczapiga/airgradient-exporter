# air gradient exporter

This is a very basic prometheus push gateway for Air Gradient DIY.

See <https://www.airgradient.com/diy/> for information on building you own.

Just modify the APIROOT and point it at this server. No modifications to the URL format are necessary.

Point prometheus at the server's `/metrics`

# installation

The root of this repo expected in `/opt/airgradient-exporter/bin`.

```
$ cp airgradient-exporter.service /etc/systemd/system
$ systemctl daemon-reload
$ systemctl status airgradient-exporter
$ systemctl enable airgradient-exporter
$ systemctl start airgradient-exporter
```

# comments

This code was written in a hurry and sent straight up to github. No optimizations were made, and it may not even work correctly. Bug fixes and improvements welcome, send a PR.

# license

```
Copyright (C) 2021   Brian Czapiga

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <http://www.gnu.org/licenses/> for more information.
```
