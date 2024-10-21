%global debug_package %{nil}

# Master definition that will be written to macro files
%global golang_arches_future x86_64 %{arm} aarch64
%global golang_arches   %{ix86} %{golang_arches_future}
%global gccgo_arches    %{golang_arches}

# Go sources can contain arch-specific files and our macros will package the
# correct files for each architecture. Therefore, move gopath to _libdir and
# make Go devel packages archful
%global gopath          %{_datadir}/gocode

Name:      go-rpm-macros
Version:   3.6.0
Release:   1
Summary:   Build-stage rpm automation for Go packages

License:   GPL-3.0-or-later
URL:       https://pagure.io/go-rpm-macros
Source:    %{name}-%{version}.tar.xz

Requires:  go-srpm-macros = %{version}-%{release}
Requires:  go-filesystem  = %{version}-%{release}
Requires:  golist

%description
This package provides build-stage rpm automation to simplify the creation of Go
language (golang) packages.

%package -n go-srpm-macros
Summary:   Source-stage rpm automation for Go packages
BuildArch: noarch

%description -n go-srpm-macros
This package provides SRPM-stage rpm automation to simplify the creation of Go
language (golang) packages.

It limits itself to the automation subset required to create Go SRPM packages
and needs to be included in the default build root.

The rest of the automation is provided by the go-rpm-macros package, that
go-srpm-macros will pull in for Go packages only.

%package -n go-filesystem
Summary:   Directories used by Go packages
License:   LicenseRef-Fedora-Public-Domain

%description -n go-filesystem
This package contains the basic directory layout used by Go packages.

%prep
%autosetup -p1 -n %{name}
%writevars -f rpm/macros.d/macros.go-srpm golang_arches golang_arches_future gccgo_arches gopath

%install
install -m 0755 -vd   %{buildroot}%{_rpmmacrodir}

install -m 0755 -vd   %{buildroot}%{_rpmluadir}/srpm
install -m 0644 -vp   %{name}/rpm/lua/srpm/*lua %{buildroot}%{_rpmluadir}/srpm

%ifarch %{golang_arches} %{gccgo_arches}
# Some of those probably do not work with gcc-go right now
# This is not intentional, but mips is not a primary Fedora architecture
# Patches and PRs are welcome

install -m 0755 -vd   %{buildroot}%{gopath}/src

install -m 0644 -vp   %{name}/rpm/macros.d/macros.go-*rpm* %{buildroot}%{_rpmmacrodir}
install -m 0755 -vd   %{buildroot}%{_rpmluadir}/fedora/rpm
install -m 0644 -vp   %{name}/rpm/lua/rpm/*lua %{buildroot}%{_rpmluadir}/fedora/rpm
install -m 0755 -vd   %{buildroot}%{_rpmconfigdir}/fileattrs
install -m 0644 -vp   %{name}/rpm/fileattrs/*.attr %{buildroot}%{_rpmconfigdir}/fileattrs/
install -m 0755 -vp   %{name}/rpm/*\.{prov,deps} %{buildroot}%{_rpmconfigdir}/

%else
install -m 0644 -vp   %{name}/rpm/macros.d/macros.go-srpm %{buildroot}%{_rpmmacrodir}
%endif

%ifarch %{golang_arches}
install -m 0644 -vp   %{name}/rpm/macros.d/macros.go-compilers-golang{,-pie} %{buildroot}%{_rpmconfigdir}/macros.d/
%endif

%ifarch %{gccgo_arches}
install -m 0644 -vp   %{name}/rpm/macros.d/macros.go-compilers-gcc %{buildroot}%{_rpmconfigdir}/macros.d/
%endif

%ifarch %{golang_arches} %{gccgo_arches}
%files
%{_rpmconfigdir}/fileattrs/*.attr
%{_rpmconfigdir}/*.prov
%{_rpmconfigdir}/*.deps
%{_rpmmacrodir}/macros.go-rpm*
%{_rpmmacrodir}/macros.go-compiler*
%{_rpmluadir}/fedora/rpm/*.lua
%{_rpmluadir}/srpm/*.lua

%files -n go-filesystem
%dir %{gopath}
%dir %{gopath}/src
%endif

%files -n go-srpm-macros
%{_rpmmacrodir}/macros.go-srpm
