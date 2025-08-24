%global debug_package %{nil}

Name:       sesh
Version:    2.17.1
Release:    %autorelease
Summary:    Smart terminal session manager for tmux
License:    MIT
URL:        https://github.com/joshmedeski/sesh
Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: golang >= 1.24
BuildRequires: git

Requires: fzf
Requires: gum
Requires: tmux
Requires: zoxide

%description
Sesh is a CLI that helps you create and manage tmux sessions quickly and easily using zoxide.

%prep
%autosetup -p1

%build
export CGO_ENABLED=0
go build -v -o sesh .

%install
install -Dpm 0755 sesh %{buildroot}%{_bindir}/sesh

%check
%{buildroot}%{_bindir}/sesh --version

%files
%license LICENSE
%doc README.md
%{_bindir}/%name

%changelog
%autochangelog
