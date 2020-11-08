.PHONY: install
.PHONY: uninstall
.PHONY: clean

install:
	export CDIR=$(shell pwd); cat ./ipython_launcher_template.sh | sed -e "s#\$$VIEWER_DIR#$$CDIR#g" > ipython_launcher.sh
	chmod a+x ./ipython_launcher.sh
	ln -s $(shell pwd)/ipython_launcher.sh /usr/local/bin/ipv

uninstall:
	unlink /usr/local/bin/ipv

clean:
	rm ./ipython_launcher.sh
