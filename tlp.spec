Summary:	Power management tool for Linux
Name:		tlp
Version:	0.3.9
Release:	1
License:	GPL v2
Group:		Base
Source0:	https://github.com/linrunner/TLP/archive/%{version}.tar.gz?/%{name}-%{version}.tar.gz
# Source0-md5:	910e2d16d669a782021c510952129505
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
	PMETC=$RPM_BUILD_ROOT%{_sysconfdir}/pm/power.d \
	TLIB=$RPM_BUILD_ROOT%{_libdir}/tlp-pm \
	PLIB=$RPM_BUILD_ROOT%{_libdir}/pm-utils \
	ULIB=$RPM_BUILD_ROOT%/lib/udev \
	ACPI=$RPM_BUILD_ROOT%{_sysconfdir}/acpi \
	NMDSP=$RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/dispatcher.d \
	CONFFILE=$RPM_BUILD_ROOT%{_sysconfdir}/default/tlp

install -d $RPM_BUILD_ROOT%{_mandir}/{man1,man8} $RPM_BUILD_ROOT%{systemdtmpfilesdir} \
	$RPM_BUILD_ROOT%{systemdunitdir} $RPM_BUILD_ROOT%{_varrun}/%{name}
install man/bluetooth.1 man/run-on-ac.1 man/run-on-bat.1 man/wifi.1 \
	man/wwan.1 $RPM_BUILD_ROOT%{_mandir}/man1
install man/tlp.8 man/tlp-stat.8 $RPM_BUILD_ROOT%{_mandir}/man8

install tlp.service $RPM_BUILD_ROOT%{systemdunitdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

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
%dir %{_libdir}/tlp-pm
%dir %{_varrun}/%{name}
%attr(755,root,root) %{_bindir}/bluetooth
%attr(755,root,root) %{_bindir}/run-on-ac
%attr(755,root,root) %{_bindir}/run-on-bat
%attr(755,root,root) %{_bindir}/tlp-pcilist
%attr(755,root,root) %{_bindir}/tlp-stat
%attr(755,root,root) %{_bindir}/tlp-usblist
%attr(755,root,root) %{_bindir}/wifi
%attr(755,root,root) %{_bindir}/wwan
%{_sysconfdir}/acpi/events/thinkpad-radiosw
%{_sysconfdir}/acpi/thinkpad-radiosw.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default/tlp
%{systemdtmpfilesdir}/%{name}.conf
%{systemdunitdir}/tlp.service
%attr(755,root,root) %{_libdir}/pm-utils/power.d/zztlp
%attr(755,root,root) %{_libdir}/pm-utils/sleep.d/49bay
%attr(755,root,root) %{_libdir}/pm-utils/sleep.d/49wwan
%attr(755,root,root) %{_libdir}/tlp-pm/tlp-functions
%attr(755,root,root) %{_libdir}/tlp-pm/tlp-nop
%attr(755,root,root) %{_libdir}/tlp-pm/tlp-rf-func
%attr(755,root,root) %{_libdir}/tlp-pm/tpacpi-bat
%{_mandir}/man1/bluetooth.1*
%{_mandir}/man1/run-on-ac.1*
%{_mandir}/man1/run-on-bat.1*
%{_mandir}/man1/wifi.1*
%{_mandir}/man1/wwan.1*
%{_mandir}/man8/tlp.8*
%{_mandir}/man8/tlp-stat.8*
%attr(755,root,root) %{_sbindir}/tlp

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/*
