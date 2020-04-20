PKGNAME=plasma-backup
#VER=0.10.5
VER=$(shell printf "%s.%s" "$(shell git rev-list --count HEAD)" "$(shell git rev-parse --short HEAD)")
REL=1

all: build

build:
	# Links
	ln -sf ../../opt/plasma/plasma-agent/main.py plasma-agent
	ln -sf ../../opt/plasma/plasma-rotate/main.py plasma-rotate
	# Build
	fpm \
		-s dir -t deb \
		-n "${PKGNAME}" -v ${VER}-${REL} \
		--deb-pre-depends=python3 \
		'../plasma-agent=/opt/plasma' \
		'../plasma-rotate=/opt/plasma' \
		'../plasma-agent.example.json=/etc/plasma-agent.json' \
		'../systemd/plasma-agent.service=/usr/lib/systemd/system/plasma-agent.service' \
		'../systemd/plasma-agent.timer=/usr/lib/systemd/system/plasma-agent.timer' \
		'plasma-agent=/usr/bin/' \
		'plasma-rotate=/usr/bin/' \

		#--after-install=postinstall.sh \
	
	rm plasma-agent plasma-rotate

#list:
#	7z x *.deb
#	7z x *data*
#	7z l data.tar

clean:
	#rm -rf ./src
	rm -f *.deb

#mrproper: clean
#	rm -f nomad_*_linux_amd64.zip

install:
	#dpkg -i ${PKGNAME}_${VER}-${REL}_amd64.deb
	apt-get install ./${PKGNAME}_${VER}-${REL}_amd64.deb

uninstall:
	dpkg --remove ${PKGNAME}
