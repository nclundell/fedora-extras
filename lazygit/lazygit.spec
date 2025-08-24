%global debug_package %{nil}

Name:       lazygit
Version:    0.54.2
Release:    %autorelease
Summary:    Simple, pragmatic TUI (Terminal UI) frontend for GIT
License:    MIT
URL:        https://github.com/jesseduffield/lazygit
Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: golang >= 1.24
BuildRequires: go-md2man

%description
Lazygit is a simple terminal UI for Git commands, written in Go. It provides an intuitive interface for managing Git repositories from the command line.

%prep
%autosetup -p1

%build
go build \
  -ldflags "-X main.version=%{version} -s -w" \
  -o _build/%{name}

%if 0%{?fedora}
go-md2man -in README.md -out %{name}.1
%endif

%install
install -Dpm 0755 _build/%{name} %{buildroot}%{_bindir}/%{name}
%if 0%{?fedora}
install -Dpm 0644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
%endif

%check
%{buildroot}%{_bindir}/%{name} --version

%files
%license LICENSE
%doc README.md CONTRIBUTING.md docs/
%{_bindir}/%{name}
%if 0%{?fedora}
%{_mandir}/man1/*.1*
%endif

%changelog
%autochangelog
