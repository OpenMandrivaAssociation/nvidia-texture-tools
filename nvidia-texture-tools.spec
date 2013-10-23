%global		soversion	2.0

Name:		nvidia-texture-tools
Version:	2.0.8
Release:	5
Summary:	Collection of image processing and texture manipulation tools
Group:		System/Libraries
License:	MIT
URL:		http://code.google.com/p/nvidia-texture-tools/
Source0:	http://nvidia-texture-tools.googlecode.com/files/%{name}-%{version}-1.tar.gz
BuildRequires:	cmake
BuildRequires:	help2man
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
# g++ 4.7 does not include unistd.h by default to avoid namespace polution
Patch0:		%{name}-%{version}-gcc4.7.patch
# use a saner type for int64 and uint64 generic typedefs that are unlikely
# to conflict with other headers that do not use long long on 64 bit
Patch1:		%{name}-%{version}-wordsize.patch
# from 0ad sources
Patch2:		%{name}-%{version}-png-api.patch
# add soversion to libraries
Patch3:		%{name}-%{version}-soversion.patch
# install libraries in proper directory
Patch4:		%{name}-%{version}-libdir.patch

%description
The NVIDIA Texture Tools is a collection of image processing and texture
manipulation tools, designed to be integrated in game tools and asset
conditioning pipelines.

The primary features of the library are mipmap and normal map generation,
format conversion and DXT compression.

DXT compression is based on Simon Brown's squish library. The library also
contains an alternative GPU-accelerated compressor that uses CUDA and is
one order of magnitude faster.

%package	devel
Summary:	Development libraries/headers for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description	devel
Headers and libraries for development with %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
sed -e 's/\r//' -i NVIDIA_*.txt

%cmake -DNVTT_SHARED=1 -DCMAKE_SKIP_RPATH=1
%make

%install
make -C build install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
pushd $RPM_BUILD_ROOT/%{_bindir}
    export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}:
    for bin in *; do
	help2man --no-info ./$bin > $RPM_BUILD_ROOT/%{_mandir}/man1/$bin.1
    done
popd

%check
make -C build filtertest

%files
%doc NVIDIA_Texture_Tools_LICENSE.txt
%doc NVIDIA_Texture_Tools_README.txt
%{_bindir}/*
%{_libdir}/lib*.%{version}
%{_libdir}/lib*.%{soversion}
%{_mandir}/man1/*

%files		devel
%doc ChangeLog
%{_includedir}/nvtt
%{_libdir}/lib*.so

%changelog
* Wed Jan 02 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.0.8-1
- Import nvidia-texture-tools.
