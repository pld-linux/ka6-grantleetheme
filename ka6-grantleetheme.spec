#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeappsver	25.08.2
%define		kf_ver		6.3.0
%define		qt_ver		6.6.0
%define		kaname		grantleetheme
Summary:	Grantlee Theme library
Summary(pl.UTF-8):	Biblioteka motywów Grantlee
Name:		ka6-%{kaname}
Version:	25.08.2
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	f3114703af49feedd079a3676c8853ad
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Network-devel >= %{qt_ver}
%if %{with tests}
BuildRequires:	Qt6Test-devel >= %{qt_ver}
%endif
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.20
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf6-kcolorscheme-devel >= %{kf_ver}
BuildRequires:	kf6-kconfig-devel >= %{kf_ver}
BuildRequires:	kf6-kguiaddons-devel >= %{kf_ver}
BuildRequires:	kf6-ki18n-devel >= %{kf_ver}
BuildRequires:	kf6-kiconthemes-devel >= %{kf_ver}
BuildRequires:	kf6-knewstuff-devel >= %{kf_ver}
BuildRequires:	kf6-ktexttemplate-devel
BuildRequires:	kf6-kxmlgui-devel >= %{kf_ver}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	kf6-kcolorscheme >= %{kf_ver}
Requires:	kf6-kconfig >= %{kf_ver}
Requires:	kf6-kguiaddons >= %{kf_ver}
Requires:	kf6-ki18n >= %{kf_ver}
Requires:	kf6-kiconthemes >= %{kf_ver}
Requires:	kf6-knewstuff >= %{kf_ver}
Requires:	kf6-kxmlgui >= %{kf_ver}
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-grantleetheme < 24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GrantleeTheme library provides a class for loading theme packages
containing set of templates.

%description -l pl.UTF-8
Biblioteka GrantleeTheme dostarcza klasę do ładowania paczek
zawierających zestawy szablonów.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kf6-ktexttemplate-devel
Obsoletes:	ka5-grantleetheme-devel < 24

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang libgrantleetheme6

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f libgrantleetheme6.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libKPim6GrantleeTheme.so.*.*.*
%ghost %{_libdir}/libKPim6GrantleeTheme.so.6
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexttemplate/kde_grantlee_plugin.so
%{_datadir}/qlogging-categories6/grantleetheme.categories
%{_datadir}/qlogging-categories6/grantleetheme.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKPim6GrantleeTheme.so
%{_includedir}/KPim6/GrantleeTheme
%{_libdir}/cmake/KPim6GrantleeTheme
