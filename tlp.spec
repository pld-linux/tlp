# TODO
# - unpackaged:
# /etc/init.d/tlp
Summary:	Power management tool for Linux
Name:		tlp
Version:	0.8
Release:	2
License:	GPL v2
Group:		Base
Source0:	https://github.com/linrunner/TLP/archive/%{version}.tar.gz?/%{name}-%{version}.tar.gz
# Source0-md5:	d53ef993ce96ccff904d6caad1f14006
Source1:	%{name}.tmpfiles
URL:		http://linrunner.de/en/tlp/tlp.html
BuildRequires:	rpmbuild(macros) >= 1.673
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
Requires:	bash-completion >= 2.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-%{name}
This package provides bash-completion for tlp.

%prep
%setup -q -n TLP-%{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install-tlp \
	DESTDIR=$RPM_BUILD_ROOT \
	TLP_SBIN=%{_sbindir} \
	TLP_BIN=%{_bindir} \
	TLP_TLIB=%{_libdir}/tlp-pm \
	TLP_PLIB=%{_libdir}/pm-utils \
	TLP_ULIB=/lib/udev \
	TLP_ACPI=/etc/acpi \
	TLP_NMDSP=/etc/NetworkManager/dispatcher.d \
	TLP_CONF=/etc/default/tlp \
	TLP_SHCPL=%{bash_compdir}

install -d $RPM_BUILD_ROOT{%{_mandir}/{man1,man8},%{systemdtmpfilesdir},%{systemdunitdir},%{_varrun}/%{name}}
cp -p man/{bluetooth,run-on-ac,run-on-bat,wifi,wwan}.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p man/{tlp,tlp-stat}.8 $RPM_BUILD_ROOT%{_mandir}/man8

cp -p tlp.service tlp-sleep.service $RPM_BUILD_ROOT%{systemdunitdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post tlp.service tlp-sleep.service

%preun
%systemd_preun tlp.service tlp-sleep.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README
/etc/acpi/events/thinkpad-radiosw
%attr(755,root,root) /etc/acpi/thinkpad-radiosw.sh
%config(noreplace) %verify(not md5 mtime size) /etc/default/tlp
/lib/udev/rules.d/85-tlp.rules
%attr(755,root,root) /lib/udev/tlp-usb-udev
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
%{systemdunitdir}/tlp-sleep.service
%dir %{_varrun}/%{name}

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/tlp
