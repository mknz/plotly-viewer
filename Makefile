.PHONY: install
.PHONY: uninstall
.PHONY: clean

install:
	apt install wmctrl chromium-browser
	export CDIR=$(shell pwd); cat ./ipython_launcher_template.sh | sed -e "s#\$$VIEWER_DIR#$$CDIR#g" > ipython_launcher.sh
	chmod a+x ./ipython_launcher.sh
	ln -s $(shell pwd)/ipython_launcher.sh /usr/local/bin/ipv
	export USER=$(shell who | cut -d ' ' -f 1); cp ./savefig.py /home/$$USER/.ipython/profile_default/startup/

uninstall:
	unlink /usr/local/bin/ipv
	export USER=$(shell who | cut -d ' ' -f 1); rm /home/$$USER/.ipython/profile_default/startup/savefig.py

clean:
	rm ./ipython_launcher.sh
