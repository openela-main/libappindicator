Name:		libappindicator
Version:	12.10.0
Release:	19%{?dist}
Summary:	Application indicators library

License:	LGPLv2 and LGPLv3
URL:		https://launchpad.net/libappindicator
Source0:	https://launchpad.net/libappindicator/12.10/%{version}/+download/%{name}-%{version}.tar.gz
Patch0:		covscan.patch
# https://bazaar.launchpad.net/~indicator-applet-developers/libappindicator/trunk.16.10/revision/285
Patch1:		incompatible_pointer_build_fix.patch
Patch2:         disable-python2.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	vala-tools
BuildRequires:	dbus-glib-devel
BuildRequires:	libdbusmenu-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk3-devel
BuildRequires:	libindicator-gtk3-devel

%description
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.


%package devel
Summary:	Development files for %{name}

Requires:	%{name} = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	libdbusmenu-devel

%description devel
This package contains the development files for the appindicator library.


%package gtk3
Summary:	Application indicators library - GTK 3

%description gtk3
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.

This package contains the GTK 3 version of this library.


%package gtk3-devel
Summary:	Development files for %{name}-gtk3

Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	libdbusmenu-devel

%description gtk3-devel
This package contains the development files for the appindicator-gtk3 library.


%package docs
Summary:	Documentation for %{name}-gtk3

BuildArch:	noarch

%description docs
This package contains the documentation for the appindicator and
appindicator-gtk3 libraries.


%prep
%autosetup -p1

sed -i "s#gmcs#mcs#g" configure.ac
# fix for gtk-doc 1.26
sed -i 's/--nogtkinit//' docs/reference/Makefile.am
gtkdocize --copy
cp -f gtk-doc.make gtk-doc.local.make
autoreconf -vif


%build
export CFLAGS="%{optflags} $CFLAGS -Wno-deprecated-declarations"
%configure --with-gtk=3 --enable-gtk-doc --disable-static
# Parallel make, crash the build
make -j1 V=1


%install
%make_install

find %{buildroot} -type f -name '*.la' -delete

%ldconfig_scriptlets gtk3


%files gtk3
%doc AUTHORS README COPYING COPYING.LGPL.2.1
%{_libdir}/libappindicator3.so.*
%{_libdir}/girepository-1.0/AppIndicator3-0.1.typelib


%files gtk3-devel
%dir %{_includedir}/libappindicator3-0.1/
%dir %{_includedir}/libappindicator3-0.1/libappindicator/
%{_includedir}/libappindicator3-0.1/libappindicator/*.h
%{_libdir}/libappindicator3.so
%{_libdir}/pkgconfig/appindicator3-0.1.pc
%{_datadir}/gir-1.0/AppIndicator3-0.1.gir
%{_datadir}/vala/vapi/appindicator3-0.1.vapi
%{_datadir}/vala/vapi/appindicator3-0.1.deps


%files docs
%doc %{_datadir}/gtk-doc/html/libappindicator/


%changelog
* Fri Jun 08 2018 Tomas Popela <tpopela@redhat.com> - 12.10.0-19
- Remove the support for gtk2 and python2

* Fri May 25 2018 Tomas Popela <tpopela@redhat.com> - 12.10.0-18
- Fix build, remove mono support

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 12.10.0-17
- Python 2 binary package renamed to python2-appindicator
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 12.10.0-13
- rebuild - mono on aarch64

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-12
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Peter Robinson <pbrobinson@fedoraproject.org> 12.10.0-9
- Rebuild (mono4)

* Sun Jan  4 2015 Peter Robinson <pbrobinson@fedoraproject.org> 12.10.0-8
- Rather than exclude the entire library from non mono arches just don't build the bindings

* Mon Dec 29 2014 Eduardo Echeverria  <echevemaster@gmail.com> - 12.10.0-7
- Added workaround -Wno-deprecated-declarations for fix FTBFS

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 12.10.0-5
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Dan Horák <dan[at]danny.cz> - 12.10.0-2
- set ExclusiveArch

* Fri May 31 2013 Eduardo Echeverria  <echevemaster@gmail.com> - 12.10.0-1
- Initial Packaging
