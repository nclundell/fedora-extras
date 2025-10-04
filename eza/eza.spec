%global debug_package %{nil}
%global bash_completions_dir %{_datadir}/bash-completion/completions
%global fish_completions_dir %{_datadir}/fish/vendor_completions.d
%global zsh_completions_dir %{_datadir}/zsh/site-functions
%global nu_completions_dir %{_datadir}/nushell/completions

Name:    eza
Version: 0.23.4
Release: %autorelease
Summary: A modern replacement for ls
License: EUPL-1.2
URL:     https://github.com/eza-community/%{name}
Source:  %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: pandoc

%description
eza is a modern, maintained replacement for the venerable file-listing
command-line program ls that ships with Unix and Linux operating systems,
giving it more features and better defaults.
It uses colours to distinguish file types and metadata.
It knows about symlinks, extended attributes, and Git.
And it’s small, fast, and just one single binary.

By deliberately making some decisions differently,
eza attempts to be a more featureful, more user-friendly version of ls.

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/%{name} -t %{buildroot}%{_bindir}/
# Man
mkdir target/man
for page in eza.1 eza_colors.5 eza_colors-explanation.5; do
    sed "s/\$version/v%{version}/g" "man/${page}.md" | pandoc --standalone -f markdown -t man > "target/man/${page}"
done;
install -Dpm 0644 target/man/eza.1 -t %{buildroot}/%{_mandir}/man1/
install -Dpm 0644 target/man/eza_colors.5 -t %{buildroot}/%{_mandir}/man5/
install -Dpm 0644 target/man/eza_colors-explanation.5 -t %{buildroot}/%{_mandir}/man5/
# Shell completions
install -Dpm 0644 completions/bash/%{name} -t %{buildroot}/%{bash_completions_dir}
install -Dpm 0644 completions/fish/%{name}.fish -t %{buildroot}/%{fish_completions_dir}
install -Dpm 0644 completions/nush/eza.nu -t %{buildroot}%{nu_completions_dir}
install -Dpm 0644 completions/zsh/_%{name} -t %{buildroot}/%{zsh_completions_dir}

%check
%{buildroot}%{_bindir}/%{name} --version

%files
%doc CHANGELOG.md README.md
%license LICENSE.txt LICENSE.summary LICENSE.dependencies
%{_bindir}/%{name}
%{_mandir}/man1/eza.1*
%{_mandir}/man5/eza_colors*
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish
%{nu_completions_dir}/eza.nu
%{zsh_completions_dir}/_%{name}

%changelog
%autochangelog
