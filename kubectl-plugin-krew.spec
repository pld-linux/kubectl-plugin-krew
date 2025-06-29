%define		vendor_version	0.4.5

Summary:	kubectl plugin manager
Name:		kubectl-plugin-krew
Version:	0.4.5
Release:	1
License:	Apache v2.0
Group:		Applications
Source0:	https://github.com/kubernetes-sigs/krew/archive/v%{version}/krew-%{version}.tar.gz
# Source0-md5:	c205efe707b700d7b0a4ce4c0af75cb8
Source1:	krew-vendor-%{vendor_version}.tar.xz
# Source1-md5:	831c8142261c637e340fe12fba4e2254
URL:		https://krew.sigs.k8s.io
BuildRequires:	golang >= 1.22
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kubectl >= 1.12
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	_debugsource_packages

%description
Krew is the plugin manager for kubectl command-line tool.

Krew helps you:
- discover kubectl plugins,
- install them on your machine,
- and keep the installed plugins up-to-date.

%prep
%setup -q -n krew-%{version} -a1

%{__mv} krew-%{vendor_version}/vendor .

%build
%__go build -v -mod=vendor -tags netgo -ldflags="-X sigs.k8s.io/krew/internal/version.gitTag=v%{version}" -o target/kubectl-krew ./cmd/krew

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p target/kubectl-krew $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md README.md docs/*.md
%attr(755,root,root) %{_bindir}/kubectl-krew
