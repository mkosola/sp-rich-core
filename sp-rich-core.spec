%define _name sp-rich-core
Name: %{_name}
Version: 1.65.1
Release: 1
Summary: Create rich core dumps
Group: Development/Tools
License: GPL-2
Source0: %{_name}-%{version}.tar.gz  
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: elfutils-libelf-devel
Requires: lzop
Requires: sp-endurance
Requires: core-reducer

%description
Tool that creates rich core dumps, which include information about system state and core in a single compressed file. Requires a kernel that supports piping core dumps. 

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/init.d/rich-core-*
/usr/sbin/rich-core-dumper

%package postproc
Summary: Rich core postprocessing
Group: Development/Tools
#Requires: lzop

%description postproc
Tools to extract information from rich cores.

%files postproc
%defattr(-,root,root,-)
%{_bindir}/rich-core-extract

%package tests
Summary: Tests for the sp-rich-core packages
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-postproc = %{version}-%{release}
Requires: core-reducer = %{version}-%{release}

%description tests
Provides test cases for sp-rich-core, sp-rich-core-postproc and core-reducer.

%files tests
%defattr(-,root,root,-)
%{_datadir}/%{name}-tests/*

%package -n core-reducer
Summary: Reduce the size of a core dump
Group: Development/Tools
Provides: core-reducer
Requires: %{name} = %{version}-%{release}
Requires: elfutils-libelf

%description -n core-reducer
Create core dumps that have a reduced size, allowing them to be transported between systems, even those with limited network throughput.

%files -n core-reducer
%defattr(-,root,root,-)
%{_bindir}/core-reducer

%prep
%setup -q -n %{name}-%{version}

%build
touch NEWS README AUTHORS ChangeLog
autoreconf --install
%configure --prefix=/usr --sysconfdir=/etc
make

%install
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}/%{_datadir}/%{name}-tests/*
make install DESTDIR=%{buildroot}
install -D -m 755 scripts/rich-core-dumper %{buildroot}/usr/sbin/
install -D -m 755 scripts/rich-core-pattern %{buildroot}/%{_sysconfdir}/init.d/

%clean
make distclean

%post  
/sbin/chkconfig --add rich-core-pattern  

%preun  
/sbin/chkconfig --del rich-core-pattern  
