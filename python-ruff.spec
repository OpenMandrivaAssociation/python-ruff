%undefine _debugsource_template
%define module ruff
%define oname ruff

# NOTE	Run create_vendored_crate_archive.sh script to create vendor archive-
# NOTE	when you update this package, submit archive to to abf and update-
# NOTE	Source1 & yml.

Name:		python-ruff
Version:	0.17.0
Release:	1
Summary:	An extremely fast Python linter and code formatter, written in Rust
License:	MIT
Group:		Development/Python
URL:		https://pypi.org/project/ruff/
Source0:	https://files.pythonhosted.org/packages/source/r/ruff/%{oname}-%{version}.tar.gz
Source1:	%{module}-%{version}-vendor.tar.xz

BuildSystem:	python
BuildOption(prep):	-p1
BuildOption(prep):	-a1
BuildRequires:	cargo
BuildRequires:	make
BuildRequires:	pkgconfig(python)
BuildRequires:	python
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	python%{pyver}dist(wheel)

%description
An extremely fast Python linter and code formatter, written in Rust.

Ruff aims to be orders of magnitude faster than alternative tools while
integrating more functionality behind a single, common interface.

%prep -a
# The crates are already vendored, so this build does not need rust-packaging.
mkdir -p .cargo
cat > .cargo/config.toml << 'EOF'
[net]
offline = true

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build -p
export CARGO_NET_OFFLINE=true
export CARGO_HOME=$PWD/.cargo
cargo tree --workspace --offline --edges no-build,no-dev,no-proc-macro \
	--prefix none --format '{l}: {p}' \
	| sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' \
	| sort -u > LICENSES.dependencies

%files
%license LICENSE LICENSES.dependencies
%{_bindir}/%{module}
%{python3_sitearch}/%{module}
%{python3_sitearch}/%{module}-%{version}.dist-info
