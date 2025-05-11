# TODO
# - unpackaged:
# /etc/init.d/tlp
Summary:	Power management tool for Linux
Name:		tlp
Version:	1.8.0
Release:	1
License:	GPL v2
Group:		Base
Source0:	https://github.com/linrunner/TLP/archive/%{version}.tar.gz?/%{name}-%{version}.tar.gz
# Source0-md5:	3e29a0e914f25c40c632ea4a49f6c0f3
Source1:	%{name}.tmpfiles
URL:		http://linrunner.de/en/tlp/tlp.html
BuildRequires:	rpmbuild(macros) >= 1.673
Requires:	hdparm
Requires:	iw
Requires:	util-linux >= 2.31
Suggests:	ethtool
Suggests:	smartmontools
Obsoletes:	bash-completion-tlp < 1.8.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TLP is a power management tool for Linux. It brings you the benefits
of advanced power management without the need to understand every
technical detail.

%prep
%setup -q -n TLP-%{version}

# All scripts here are bash scripts
find ./ -type f -print0 | xargs -0 %{__sed} -i -e '1s,/bin/sh$,%{__bash},'

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install-tlp install-man-tlp \
	DESTDIR=$RPM_BUILD_ROOT \
	TLP_SBIN=%{_sbindir} \
	TLP_BIN=%{_bindir} \
	TLP_FLIB=%{_datadir}/tlp/func.d \
	TLP_TLIB=%{_datadir}/tlp \
	TLP_ULIB=/lib/udev \
	TLP_NMDSP=/etc/NetworkManager/dispatcher.d \
	TLP_SYSD=%{systemdunitdir} \
	TLP_SHCPL=%{bash_compdir} \
	TLP_FISHCPL=%{fish_compdir} \
	TLP_ZSHCPL=%{zsh_compdir} \

install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post tlp.service

%preun
%systemd_preun tlp.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS changelog README.rst
%config(noreplace) %verify(not md5 mtime size) /etc/tlp.conf
%dir /etc/tlp.d
%config(noreplace) %verify(not md5 mtime size) /etc/tlp.d/00-template.conf
/etc/tlp.d/README
/lib/udev/rules.d/85-tlp.rules
%attr(755,root,root) /lib/udev/tlp-usb-udev
%attr(755,root,root) %{_bindir}/bluetooth
%attr(755,root,root) %{_bindir}/nfc
%attr(755,root,root) %{_bindir}/run-on-ac
%attr(755,root,root) %{_bindir}/run-on-bat
%attr(755,root,root) %{_bindir}/tlp-stat
%attr(755,root,root) %{_bindir}/wifi
%attr(755,root,root) %{_bindir}/wwan
%attr(755,root,root) %{_sbindir}/tlp
%{_mandir}/man1/bluetooth.1*
%{_mandir}/man1/nfc.1*
%{_mandir}/man1/run-on-ac.1*
%{_mandir}/man1/run-on-bat.1*
%{_mandir}/man1/wifi.1*
%{_mandir}/man1/wwan.1*
%{_mandir}/man8/tlp.8*
%{_mandir}/man8/tlp-stat.8*
%{_mandir}/man8/tlp.service.8*
%{systemdtmpfilesdir}/%{name}.conf
%{systemdunitdir}/tlp.service
%attr(755,root,root) /usr/lib/systemd/system-sleep/tlp
%dir /var/lib/%{name}
%dir %{_datadir}/tlp
%{_datadir}/tlp/defaults.conf
%{_datadir}/tlp/deprecated.conf
%{_datadir}/tlp/rename.conf
%attr(755,root,root) %{_datadir}/tlp/tlp-func-base
%attr(755,root,root) %{_datadir}/tlp/tlp-pcilist
%attr(755,root,root) %{_datadir}/tlp/tlp-readconfs
%attr(755,root,root) %{_datadir}/tlp/tlp-usblist
%{_datadir}/tlp/bat.d
%{_datadir}/tlp/func.d
%{_datadir}/metainfo/de.linrunner.tlp.metainfo.xml

%{bash_compdir}/bluetooth
%{bash_compdir}/nfc
%{bash_compdir}/run-on-ac
%{bash_compdir}/run-on-bat
%{bash_compdir}/tlp
%{bash_compdir}/tlp-stat
%{bash_compdir}/wifi
%{bash_compdir}/wwan

%{fish_compdir}/bluetooth.fish
%{fish_compdir}/nfc.fish
%{fish_compdir}/run-on-ac.fish
%{fish_compdir}/run-on-bat.fish
%{fish_compdir}/tlp.fish
%{fish_compdir}/tlp-stat.fish
%{fish_compdir}/wifi.fish
%{fish_compdir}/wwan.fish

%{zsh_compdir}/_tlp
%{zsh_compdir}/_tlp-radio-device
%{zsh_compdir}/_tlp-run-on
%{zsh_compdir}/_tlp-stat
