%global debug_package %{nil}

Name:    termscp
Version: 0.18.0
Release: %autorelease
Summary: A feature-rich terminal SCP client
License: MIT
URL:     https://github.com/veeso/%{name}
Source:  %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: pandoc
BuildRequires: pkg-config
BuildRequires: dbus-devel
BuildRequires: libsmbclient-devel
BuildRequires: openssl-devel
BuildRequires: perl
BuildRequires: zlib-devel

%description
A feature rich terminal UI file transfer and explorer with support for SCP/SFTP/FTP/S3/SMB

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/termscp -t %{buildroot}%{_bindir}/
mkdir target/man
sed "s/\$version/v%{version}/g" "docs/man.md" | pandoc --standalone -f markdown -t man > "target/man/termscp.1"
install -Dpm 0644 target/man/termscp.1 %{buildroot}%{_mandir}/man1/termscp.1

%check
%{buildroot}%{_bindir}/termscp --version

%files
%doc README.md CHANGELOG.md
%{_mandir}/man1/termscp.1*
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/termscp

%changelog
%autochangelog
