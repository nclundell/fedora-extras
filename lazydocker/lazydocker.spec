%global debug_package %{nil}

Name:       lazydocker
Version: 0.24.4
Release:    %autorelease
Summary:    The lazier way to manage everything docker
License:    MIT
URL:        https://github.com/jesseduffield/lazydocker
Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: golang >= 1.24
BuildRequires: go-md2man

%description
A simple terminal UI for both docker and docker-compose, written in Go.

%prep
%autosetup -p1

%build
go build \
    -ldflags "-X main.version=%{version} -s -w" \
    -o _build/%{name}

# Generate Man page
go-md2man -in README.md -out %{name}.1

%install
install -Dpm 0755 _build/%{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%check
%{buildroot}%{_bindir}/%{name} --version

%files
%doc README.md CONTRIBUTING.md docs/
%license LICENSE
%{_bindir}/%{name}
%{_mandir}/man1/*.1*

%changelog
%autochangelog
