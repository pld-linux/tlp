# TODO
# - unpackaged:
# /etc/init.d/tlp
Summary:	Power management tool for Linux
Name:		tlp
Version:	0.3.10.1
Release:	1
License:	GPL v2
Group:		Base
Source0:	https://github.com/linrunner/TLP/archive/%{version}.tar.gz?/%{name}-%{version}.tar.gz
# Source0-md5:	38c05b11e9c77838f263c4ae5fd45788
Source1:	%{name}.tmpfiles
URL:		http://linrunner.de/en/tlp/tlp.html
Requires:	acpid
Requires:	ethtool
Requires:	hdparm
Requires:	pm-utils
Requires:	rfkill
Requires:	wireless-tools
Suggests:	bash-completion-%{name}
Suggests:	smartmontools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TLP is a power management tool for Linux. It brings you the benefits
of advanced power management without the need to understand every
technical detail.

%package -n bash-completion-%{name}
Summary:	bash-completion for tlp
Group:		Applications/Shells
Requires:	bash-completion

%description -n bash-completion-%{name}
This package provides bash-completion for tlp.

%prep
%setup -q -n TLP-%{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install-tlp \
	DESTDIR=$RPM_BUILD_ROOT \
	SBIN=$RPM_BUILD_ROOT%{_sbindir} \
	BIN=$RPM_BUILD_ROOT%{_bindir} \
	PMETC=$RPM_BUILD_ROOT/etc/pm/power.d \
	TLIB=$RPM_BUILD_ROOT%{_libdir}/tlp-pm \
	PLIB=$RPM_BUILD_ROOT%{_libdir}/pm-utils \
	ULIB=$RPM_BUILD_ROOT/lib/udev \
	ACPI=$RPM_BUILD_ROOT/etc/acpi \
	NMDSP=$RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d \
	CONFFILE=$RPM_BUILD_ROOT/etc/default/tlp

install -d $RPM_BUILD_ROOT{%{_mandir}/{man1,man8},%{systemdtmpfilesdir},%{systemdunitdir},%{_varrun}/%{name}}
cp -p man/{bluetooth,run-on-ac,run-on-bat,wifi,wwan}.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p man/{tlp,tlp-stat}.8 $RPM_BUILD_ROOT%{_mandir}/man8

cp -p tlp.service $RPM_BUILD_ROOT%{systemdunitdir}
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
%doc README
/etc/acpi/events/thinkpad-radiosw
%attr(755,root,root) /etc/acpi/thinkpad-radiosw.sh
%config(noreplace) %verify(not md5 mtime size) /etc/default/tlp
/lib/udev/rules.d/40-tlp.rules
/lib/udev/tlp-usb-udev
%attr(755,root,root) %{_bindir}/bluetooth
%attr(755,root,root) %{_bindir}/run-on-ac
%attr(755,root,root) %{_bindir}/run-on-bat
%attr(755,root,root) %{_bindir}/tlp-pcilist
%attr(755,root,root) %{_bindir}/tlp-stat
%attr(755,root,root) %{_bindir}/tlp-usblist
%attr(755,root,root) %{_bindir}/wifi
%attr(755,root,root) %{_bindir}/wwan
%attr(755,root,root) %{_sbindir}/tlp
%{_mandir}/man1/bluetooth.1*
%{_mandir}/man1/run-on-ac.1*
%{_mandir}/man1/run-on-bat.1*
%{_mandir}/man1/wifi.1*
%{_mandir}/man1/wwan.1*
%{_mandir}/man8/tlp.8*
%{_mandir}/man8/tlp-stat.8*
%attr(755,root,root) %{_libdir}/pm-utils/sleep.d/49tlp
%dir %{_libdir}/tlp-pm
%attr(755,root,root) %{_libdir}/tlp-pm/tlp-functions
%attr(755,root,root) %{_libdir}/tlp-pm/tlp-nop
%attr(755,root,root) %{_libdir}/tlp-pm/tlp-rf-func
%attr(755,root,root) %{_libdir}/tlp-pm/tpacpi-bat
%{systemdtmpfilesdir}/%{name}.conf
%{systemdunitdir}/tlp.service
%dir %{_varrun}/%{name}

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/*
