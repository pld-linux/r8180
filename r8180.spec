#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	Linux driver for WLAN card base on RTL8180
Summary(pl.UTF-8):   Sterownik dla Linuksa do kart bezprzewodowych na układzie RTL8180
Name:		r8180
Version:	0.15
%define		_rel	1
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/rtl8180-sa2400/rtl8180-%{version}.tar.gz
Patch0:		%{name}-linux26.patch
URL:		http://rtl8180-sa2400.sourceforge.net/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%package -n kernel-net-r8180
Summary:	Linux driver for WLAN card base on RTL8180
Summary(pl.UTF-8):   Sterownik dla Linuksa do kart bezprzewodowych na układzie RTL8180
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description
This is driver for WLAN card based on RTL8180 for Linux.

%description -l pl.UTF-8
Sterownik dla Linuksa do kart WLAN opartych o układ RTL8180.

%description -n kernel-net-r8180
This is driver for WLAN card based on RTL8180 for Linux.

%description -n kernel-net-r8180 -l pl.UTF-8
Sterownik dla Linuksa do kart WLAN opartych o układ RTL8180.

%package -n kernel-smp-net-r8180
Summary:	Linux driver for WLAN card base on RTL8180
Summary(pl.UTF-8):   Sterownik dla Linuksa do kart bezprzewodowych na układzie RTL8180
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-r8180
This is driver for WLAN card based on RTL8180 for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-net-r8180 -l pl.UTF-8
Sterownik dla Linuksa do kart WLAN opartych o układ RTL8180.

Ten pakiet zawiera moduł jądra Linuksa SMP.

%prep
%setup -q -n rtl8180-%{version}
%patch0 -p1

%build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean modules \
		RCS_FIND_IGNORE="-name '*.ko' -o -name priv_part.o -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	mv r8180.ko r8180-$cfg.ko
	mv ieee80211.ko ieee80211-$cfg.ko
	mv ieee80211_crypt.ko ieee80211_crypt-$cfg.ko
	mv ieee80211_crypt_wep.ko ieee80211_crypt_wep-$cfg.ko
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install r8180-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/r8180.ko
install ieee80211-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ieee80211.ko
install ieee80211_crypt-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ieee80211_crypt.ko
install ieee80211_crypt_wep-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ieee80211_crypt_wep.ko
%if %{with smp} && %{with dist_kernel}
install r8180-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/r8180.ko
install ieee80211-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/ieee80211.ko
install ieee80211_crypt-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/ieee80211_crypt.ko
install ieee80211_crypt_wep-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/ieee80211_crypt_wep.ko
%endif
%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-net-r8180
%depmod %{_kernel_ver}

%postun -n kernel-net-r8180
%depmod %{_kernel_ver}

%post -n kernel-smp-net-r8180
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-r8180
%depmod %{_kernel_ver}smp

%files -n kernel-net-r8180
%defattr(644,root,root,755)
%doc README
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-r8180
%defattr(644,root,root,755)
%doc README
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
