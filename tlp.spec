# TODO
# - unpackaged:
# /etc/init.d/tlp
Summary:	Power management tool for Linux
Name:		tlp
Version:	1.2.2
Release:	1
License:	GPL v2
Group:		Base
Source0:	https://github.com/linrunner/TLP/archive/%{version}.tar.gz?/%{name}-%{version}.tar.gz
# Source0-md5:	23dc1b2edcf4d01a37c67b12f023df22
Source1:	%{name}.tmpfiles
URL:		http://linrunner.de/en/tlp/tlp.html
BuildRequires:	rpmbuild(macros) >= 1.673
Requires:	acpid
Requires:	ethtool
Requires:	hdparm
Requires:	pm-utils
Requires:	util-linux >= 2.31
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
	TLP_FLIB=%{_datadir}/tlp/func.d \
	TLP_TLIB=%{_datadir}/tlp \
	TLP_ULIB=/lib/udev \
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
%doc AUTHORS changelog README.md
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
%{systemdtmpfilesdir}/%{name}.conf
%{systemdunitdir}/tlp.service
%{systemdunitdir}/tlp-sleep.service
%dir %{_varrun}/%{name}
%dir %{_datadir}/tlp
%attr(755,root,root) %{_datadir}/tlp/tlp-func-base
%attr(755,root,root) %{_datadir}/tlp/tpacpi-bat
%{_datadir}/tlp/func.d
%{_datadir}/metainfo/de.linrunner.tlp.metainfo.xml

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/bluetooth
%{bash_compdir}/tlp
%{bash_compdir}/tlp-stat
%{bash_compdir}/wifi
%{bash_compdir}/wwan
