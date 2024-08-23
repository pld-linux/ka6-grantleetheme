#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.08.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		grantleetheme
Summary:	Grantlee Theme
Name:		ka6-%{kaname}
Version:	24.08.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	dc216cfc7d07c04273b93ec8ad9e0a36
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	grantlee-qt6-devel >= 5.3
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-knewstuff-devel >= %{kframever}
BuildRequires:	kf6-ktexttemplate-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	ka5-%{kaname} < %{version}
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
Obsoletes:	ka5-%{kaname}-devel < %{version}

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

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKPim6GrantleeTheme.so.*.*
%ghost %{_libdir}/libKPim6GrantleeTheme.so.6
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexttemplate/kde_grantlee_plugin.so
%{_datadir}/qlogging-categories6/grantleetheme.categories
%{_datadir}/qlogging-categories6/grantleetheme.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/GrantleeTheme
%{_libdir}/cmake/KPim6GrantleeTheme
%{_libdir}/libKPim6GrantleeTheme.so

