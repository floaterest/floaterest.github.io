plan = iosevka

install = sudo apt-get update && sudo apt-get install --no-install-recommends -y $(1)
clone = git clone https://github.com/$(1).git --depth 1

autohint := $(call install,ttfautohint)

.ONESHELL: # allow cd
.PHONY: iosevka kosugi iokosu nerd-dep nerd unrename

# build iosevka
iosevka:
	$(call install,ttfautohint)
	cd Iosevka
	npm ci
	npm run build -- ttf::$(plan)
	npm run build -- webfont::$(plan)

# build kosugi-maru
kosugi:
	$(call clone,googlefonts/kosugi-maru)
	$(MAKE) -C kosugi-maru build
	mkdir -p fonts
	cp kosugi-maru/fonts/ttf/KosugiMaru-Regular.ttf fonts/kosugi-maru.ttf
	cp kosugi-maru/fonts/webfonts/KosugiMaru-Regular.woff2  fonts/kosugi-maru.woff2

# merge iosevka and kosugi-maru
iokosu:
	$(call install,fontforge)
	fontforge merge.py iosevka/iosevka-regular.ttf kosugi/kosugi-maru.ttf iokosu.ttf
