%global srcname       hamster
%global srcname_upper Hamster

%global srcurl  https://github.com/project%{srcname}/%{srcname}

Name:       %{srcname}-time-tracker
Version:    3.0.3
Release:    1%{?dist}
Summary:    The Linux time tracker

License:    GPLv3+
URL:        http://project%{srcname}.wordpress.com/
Source0:    %{srcurl}/archive/v%{version}.tar.gz#/hamster-%{version}.tar.gz
Source1:    %{name}.appdata.xml

BuildArch:        noarch

BuildRequires:    gettext intltool itstool yelp
BuildRequires:    python3-devel python3-pyxdg python3-cairo python3-gobject python3-dbus
BuildRequires:    glib2-devel desktop-file-utils

Requires:         dbus
Requires:         hicolor-icon-theme
Requires:         bash-completion

Requires:         python3-pyxdg

BuildRequires:    GConf2
Requires(pre):    GConf2
Requires(post):   GConf2
Requires(preun):  GConf2


%description
Project %{srcname} is time tracking for individuals. It helps you to keep track on
how much time you have spent during the day on activities you choose to track. 

Whenever you change from doing one task to other, you change your current
activity in %{srcname}. After a while you can see how many hours you have spent on
what. Maybe print it out, or export to some suitable format, if time reporting
is a request of your employee. 

%prep
%autosetup -p1 -n%{srcname}-%{version}
# remove shebang
sed -ibackup '1d' src/%{srcname}/overview.py # src/%{srcname}/today.py
sed -ibackup 's@#!/usr/bin/env python@#!/usr/bin/env python3@g' waf

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LINKFLAGS="-Wl,-z,relro"
./waf configure -vv --prefix=%{_prefix} --datadir=%{_datadir} 
./waf build -vv %{?_smp_mflags}

%install
./waf install --destdir=%{buildroot}
install -p -m0644 %{SOURCE1} -D %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop

%pre
%gconf_schema_prepare %{name}
%gconf_schema_obsolete %{name}

%post
%gconf_schema_upgrade %{name}

%preun
%gconf_schema_remove %{name}

# fails
# %files -f %{name}.lang
%files
%license COPYING
%doc AUTHORS MAINTAINERS README.md
%{_bindir}/%{srcname}*
%{python3_sitelib}/%{srcname}
%{_datadir}/%{srcname}/
%{_datadir}/dbus-1/services/*%{srcname_upper}*.service
%{_libexecdir}/%{srcname}/%{srcname}-service
%{_libexecdir}/%{srcname}/%{srcname}-windows-service

# schema and bash completion files do not need to be %%config
%{_datadir}/bash-completion/completions/%{srcname}.bash
%{_datadir}/glib-2.0/schemas/*

%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*%{srcname_upper}*.*

# FIXME not sure about ownership for gnome/help
%{_datadir}/help/*/%{srcname}/*

%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/metainfo/*%{srcname_upper}*.xml

%{_datadir}/locale/*/LC_MESSAGES/%{srcname}.mo

%changelog
* Mon Nov 27 2023 Lukas Doktor <ldoktor@redhat.com> - 3.0.3
- Fix python->python3 on the waf file
- desktop-file-utils dependency

* Mon Jun 15 2020 Markus Neteler <neteler@mundialis.de> - 3.0.2
- New upstream version
- updated SPEC to Python3 and new file locations

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.16.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.15.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0-0.14.rc1
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.13.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 09 2017 Iryna Shcherbina <ishcherb@redhat.com> - 2.0-0.12.rc1
- Add a build-time dependency on python2-devel (rhbz#1479813)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.11.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.10.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.9.rc1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Mar 21 2016 Raphael Groner <projects.rg@smart.ms> - 2.0-0.8.rc1
- ugly workaround for different package name in f22 to satisfy depcheck

* Sat Mar 12 2016 Raphael Groner <projects.rg@smart.ms> - 2.0-0.7.rc1
- fix version warning and TargetFlags, rhbz#1317087
- consolidate patches to same patch level and use autosetup macro

* Sat Mar 12 2016 Raphael Groner <projects.rg@smart.ms> - 2.0-0.6.rc1
- add R: python-gobject, rhbz#1316230

* Thu Mar 03 2016 Raphael Groner <projects.rg@smart.ms> - 2.0-0.5.rc1
- apply patch against ZeroDivisionError, rhbz#1309613

* Mon Feb 15 2016 Raphael Groner <projects.rg@smart.ms> - 2.0-0.4.rc1
- readd lost build conditional for epel, rhbz#1046077

* Mon Feb 15 2016 Raphael Groner <projects.rg@smart.ms> - 2.0-0.3.rc1
- add upstream patches for GNOME 3.18, rhbz#1074967, rhbz#1307256

* Tue Feb 02 2016 Raphael Groner <projects.rg@smart.ms> - 2.0-0.2.rc1
- R: dbus-python, rhbz#1285405

* Mon Dec 21 2015 Raphael Groner <projects.rg@smart.ms> - 2.0-0.1.rc1
- bump to version 2.0-rc1
- small modernization

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Nov 23 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.04-4
- Patch for rhbz#1074967

* Tue Jul 15 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.04-3
- Add requires on pyxdg

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.04-1
- Update to latest upstream release. 

* Mon Dec 30 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-6
- Update desktop-file-validate command for F19

* Sat Dec 28 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-5
- Add patch for notification fix
- rhbz#1046991
- upstream issue #127
- upstream issue #117

* Tue Dec 24 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-4
- Add wnck dependency so users can use workspaces out of the box
- https://bugzilla.redhat.com/show_bug.cgi?id=1046077

* Tue Dec 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-3
- Add missing gnome-python2-gconf requirement
- https://bugzilla.redhat.com/show_bug.cgi?id=1043564

* Mon Dec 02 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-2
- Fixes as per rhbz#1036254
- Correct schame functions
- Own gnome help dir
- Own bash completion dir
- schema and bash completion files do not need to be %%config
- https://lists.fedoraproject.org/pipermail/packaging/2013-December/009834.html

* Sat Nov 30 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-1
- Initial rpm build

